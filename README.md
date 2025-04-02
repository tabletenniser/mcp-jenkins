# MCP Jenkins
MCP server that integrates Jenkins 

## Installation
```
pip install mcp-jenkins
```

## Usage

### Inspector
```
npx @modelcontextprotocol/inspector uv run mcp-jenkins --jenkins-url xxx --jenkins-username xxx --jenkins-password xxx
```

### Used by AutoGen
```python
import asyncio

from autogen_ext.tools.mcp import StdioMcpToolAdapter, StdioServerParams
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken


async def main() -> None:
    # Create server params for the remote MCP service
    server_params = StdioServerParams(
        command='uv',
        args=[
            'run',
            'mcp-jenkins',
            '--jenkins-username',
            'xxx',
            '--jenkins-password',
            'xxx',
            '--jenkins-url',
            'xxx'
        ],
    )

    # Get the translation tool from the server
    adapter = await StdioMcpToolAdapter.from_server_params(server_params, 'get_all_jobs')

    # Create an agent that can use the translation tool
    agent = AssistantAgent(
        name='jenkins_assistant',
        model_client=[Replace_with_your_model_client],
        tools=[adapter],
    )

    # Let the agent translate some text
    await Console(
        agent.run_stream(task='Get all jobs', cancellation_token=CancellationToken())
    )


if __name__ == "__main__":
    asyncio.run(main())
```

### Optional Arguments
- `--jenkins-timeout`: Timeout for Jenkins API requests, default is 5 seconds


## Available Tools

| Tool           | Description                  |
|----------------|------------------------------|
| get_all_jobs   | Get all jobs                 |
| get_job_config | Get job config               |
| search_jobs    | Search job by specific field |
