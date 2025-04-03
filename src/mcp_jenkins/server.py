import json
import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .jenkins import JenkinsClient


@dataclass
class JenkinsContext:
    client: JenkinsClient


@asynccontextmanager
async def jenkins_lifespan(server: Server) -> AsyncIterator[JenkinsContext]:
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


app = Server('mcp-jenkins', lifespan=jenkins_lifespan)


@app.list_tools()
async def list_tools() -> list[Tool]:
    tools = []
    tools.extend([
        Tool(
            name='get_all_jobs',
            description='Get all jobs',
            inputSchema={
                'type': 'object',
                'properties': {
                    'refresh': {
                        'type': 'boolean',
                        'description': 'Weather to refresh the jobs list'
                    }
                }
            }
        ),
        Tool(
            name='get_job_config',
            description='Get job config',
            inputSchema={
                'type': 'object',
                'properties': {
                    'fullname': {
                        'type': 'string',
                        'description': 'The fullname of the job'
                    }
                }
            }
        ),
        Tool(
            name='search_jobs',
            description='Search job by specific field',
            inputSchema={
                'type': 'object',
                'properties': {
                    'class_pattern': {
                        'type': 'string',
                        'description': 'The pattern of the _class'
                    },
                    'name_pattern': {
                        'type': 'string',
                        'description': 'The pattern of the name'
                    },
                    'fullname_pattern': {
                        'type': 'string',
                        'description': 'The pattern of the fullname'
                    },
                    'url_pattern': {
                        'type': 'string',
                        'description': 'The pattern of the url'
                    },
                    'color_pattern': {
                        'type': 'string',
                        'description': 'The pattern of the color'
                    },
                    'refresh': {
                        'type': 'boolean',
                        'description': 'Weather to refresh the jobs list'
                    }
                }
            }
        )
    ])

    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """
    Handle tool calls for Jenkins operations
    """
    ctx = app.request_context.lifespan_context

    if name == 'get_all_jobs':
        refresh = arguments.get('refresh', False)

        jobs = ctx.client.get_all_jobs(refresh=refresh)

        return [
            TextContent(
                type='text',
                text=json.dumps([job.model_dump(by_alias=True) for job in jobs], indent=2, ensure_ascii=False)
            )
        ]

    elif name == 'get_job_config':
        fullname = arguments.get('fullname')

        config = ctx.client.get_job_config(fullname)

        return [
            TextContent(
                type='text',
                text=config
            )
        ]

    elif name == 'search_jobs':
        class_pattern = arguments.get('class_pattern')
        name_pattern = arguments.get('name_pattern')
        fullname_pattern = arguments.get('fullname_pattern')
        url_pattern = arguments.get('url_pattern')
        color_pattern = arguments.get('color_pattern')
        refresh = arguments.get('refresh', False)

        jobs = ctx.client.search_jobs(
            class_pattern=class_pattern,
            name_pattern=name_pattern,
            fullname_pattern=fullname_pattern,
            url_pattern=url_pattern,
            color_pattern=color_pattern,
            refresh=refresh
        )

        return [
            TextContent(
                type='text',
                text=json.dumps([job.model_dump(by_alias=True) for job in jobs], indent=2, ensure_ascii=False)
            )
        ]


async def run_server() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, write_stream, app.create_initialization_options()
        )
