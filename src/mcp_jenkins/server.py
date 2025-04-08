import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from mcp.server.fastmcp import Context, FastMCP

from .jenkins import JenkinsClient
from .models.build import Build
from .models.job import JobBase


@dataclass
class JenkinsContext:
    client: JenkinsClient


@asynccontextmanager
async def jenkins_lifespan(server: FastMCP) -> AsyncIterator[JenkinsContext]:
    try:
        jenkins_url = os.getenv('jenkins_url')
        jenkins_username = os.getenv('jenkins_username')
        jenkins_password = os.getenv('jenkins_password')
        jenkins_timeout = int(os.getenv('jenkins_timeout'))

        client = JenkinsClient(
            url=jenkins_url,
            username=jenkins_username, password=jenkins_password,
            timeout=jenkins_timeout
        )

        # Provide context to the application
        yield JenkinsContext(client=client)
    finally:
        # Cleanup resources if needed
        pass


mcp = FastMCP('mcp-jenkins', lifespan=jenkins_lifespan)


def _client(ctx: Context) -> JenkinsClient:
    return ctx.request_context.lifespan_context.client


@mcp.tool()
async def get_all_jobs(ctx: Context) -> list[JobBase]:
    """
    Get all jobs from Jenkins

    Returns:
        list[JobBase]: A list of all jobs
    """
    return _client(ctx).job.get_all_jobs()


@mcp.tool()
async def get_job_config(ctx: Context, fullname: str) -> str:
    """
    Get specific job config from Jenkins

    Args:
        fullname: The fullname of the job

    Returns:
        str: The config of the job
    """
    return _client(ctx).job.get_job_config(fullname)


@mcp.tool()
async def search_jobs(
        ctx: Context,
        class_pattern: str = None,
        name_pattern: str = None,
        fullname_pattern: str = None,
        url_pattern: str = None,
        color_pattern: str = None,
) -> list[JobBase]:
    """
    Search job by specific field

    Args:
        class_pattern: The pattern of the _class
        name_pattern: The pattern of the name
        fullname_pattern: The pattern of the fullname
        url_pattern: The pattern of the url
        color_pattern: The pattern of the color

    Returns:
        list[JobBase]: A list of all jobs
    """
    return _client(ctx).job.search_jobs(
        class_pattern=class_pattern,
        name_pattern=name_pattern,
        fullname_pattern=fullname_pattern,
        url_pattern=url_pattern,
        color_pattern=color_pattern,
    )


@mcp.tool()
async def get_running_builds(ctx: Context) -> list[Build]:
    """
    Get all running builds from Jenkins

    Returns:
        list[Build]: A list of all running builds
    """
    return _client(ctx).build.get_running_builds()


@mcp.tool()
async def get_build_info(ctx: Context, fullname: str, build_number: int | None = None) -> Build | str:
    """
    Get specific build info from Jenkins

    Args:
        fullname: The fullname of the job
        build_number: The number of the build, if None, get the last build

    Returns:
        Build: The build info
    """
    client = _client(ctx)
    if build_number is None:
        build_number = client.job._jenkins.get_job_info(fullname)['lastBuild']['number']
    return client.build.get_build_info(fullname, build_number)
