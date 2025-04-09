from mcp.server.fastmcp import Context

from mcp_jenkins.models.build import Build
from mcp_jenkins.server import mcp, client


@mcp.tool()
async def get_running_builds(ctx: Context) -> list[Build]:
    """
    Get all running builds from Jenkins

    Returns:
        list[Build]: A list of all running builds
    """
    return client(ctx).build.get_running_builds()


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
    if build_number is None:
        build_number = client(ctx).job._jenkins.get_job_info(fullname)['lastBuild']['number']
    return client(ctx).build.get_build_info(fullname, build_number)
