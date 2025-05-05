import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP

from mcp_jenkins.jenkins import JenkinsClient


def normalize_url(url: str) -> str:
    """Normalize a URL by adding a backslash at the end if it doesn't have it."""
    if not url or len(url) == 0:
        return ''
    if url[-1] != '/':
        return url + '/'
    return url


@dataclass
class JenkinsContext:
    clients: list[JenkinsClient]
    current_client_index: int = 0

    def get_client(self, index: int = None) -> JenkinsClient:
        """Get a Jenkins client by index, or the current one if no index is provided."""
        if index is not None and 0 <= index < len(self.clients):
            return self.clients[index]
        return self.clients[self.current_client_index]

    def switch_client(self, index: int) -> JenkinsClient:
        """Switch the current client to the one at the specified index."""
        if 0 <= index < len(self.clients):
            self.current_client_index = index
            return self.clients[self.current_client_index]
        error_message = f'Jenkins client index {index} out of range (0-{len(self.clients) - 1})'
        raise IndexError(error_message)

    def find_client_by_url(self, url: str) -> JenkinsClient | None:
        """Find a Jenkins client by its URL."""
        for client in self.clients:
            if url in normalize_url(client._jenkins.server):
                return client
        return None


@asynccontextmanager
async def jenkins_lifespan(server: FastMCP) -> AsyncIterator[JenkinsContext]:
    try:
        # Check if we're using multiple Jenkins instances
        jenkins_count = int(os.getenv('jenkins_count', '1'))

        clients = []
        for i in range(jenkins_count):
            # For backward compatibility with single Jenkins instance
            if jenkins_count == 1 and os.getenv('jenkins_url') is not None:
                jenkins_url = os.getenv('jenkins_url')
                jenkins_username = os.getenv('jenkins_username')
                jenkins_password = os.getenv('jenkins_password')
                jenkins_timeout = int(os.getenv('jenkins_timeout', '5'))
            else:
                jenkins_url = os.getenv(f'jenkins_url_{i}')
                jenkins_username = os.getenv(f'jenkins_username_{i}')
                jenkins_password = os.getenv(f'jenkins_password_{i}')
                jenkins_timeout = int(os.getenv(f'jenkins_timeout_{i}', '5'))

            client = JenkinsClient(
                url=jenkins_url,
                username=jenkins_username,
                password=jenkins_password,
                timeout=jenkins_timeout,
            )
            clients.append(client)

        # Provide context to the application
        yield JenkinsContext(clients=clients)
    finally:
        # Cleanup resources if needed
        pass


def client(ctx: Context, cluster_url: str = None) -> JenkinsClient:
    """
    Get a Jenkins client by URL or the current one if no URL is provided.

    Args:
        ctx: The request context
        cluster_url: Optional URL to a specific Jenkins cluster

    Returns:
        A Jenkins client
    """
    jenkins_context = ctx.request_context.lifespan_context

    if cluster_url:
        found_client = jenkins_context.find_client_by_url(cluster_url)
        if found_client:
            return found_client

    return jenkins_context.get_client()


def get_client(ctx: Context, index: int = None) -> JenkinsClient:
    """Get a Jenkins client by index, or the current one if no index is provided."""
    return ctx.request_context.lifespan_context.get_client(index)


def switch_client(ctx: Context, index: int) -> JenkinsClient:
    """Switch the current client to the one at the specified index."""
    return ctx.request_context.lifespan_context.switch_client(index)


mcp = FastMCP('mcp-jenkins', lifespan=jenkins_lifespan)


# Import the job and build modules here to avoid circular imports
from mcp_jenkins.server import build, job  # noqa: E402, F401
