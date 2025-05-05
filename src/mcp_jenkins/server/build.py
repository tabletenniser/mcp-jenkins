from mcp.server.fastmcp import Context

from mcp_jenkins.server import client, mcp


@mcp.tool()
async def get_running_builds(ctx: Context, cluster_url: str = None) -> list[dict]:
    """
    Get all running builds from Jenkins

    Args:
        cluster_url: Optional URL to a specific Jenkins cluster

    Returns:
        list[Build]: A list of all running builds
    """
    return [build.model_dump(exclude_none=True) for build in client(ctx, cluster_url).build.get_running_builds()]


@mcp.tool()
async def get_build_info(ctx: Context, fullname: str, build_number: str = None, cluster_url: str = None) -> dict:
    """
    Get specific build info from Jenkins

    Args:
        fullname: The fullname of the job
        build_number: The number of the build, if None, get the last build
        cluster_url: Optional URL to a specific Jenkins cluster

    Returns:
        Build: The build info
    """
    jenkins_client = client(ctx, cluster_url)
    if build_number is None:
        build_number = jenkins_client.job.get_job_info(fullname).lastBuild.number
    return jenkins_client.build.get_build_info(fullname, int(build_number)).model_dump(exclude_none=True)


@mcp.tool()
async def build_job(ctx: Context, fullname: str, parameters: dict = None, cluster_url: str = None) -> int:
    """
    Build a job in Jenkins

    Args:
        fullname: The fullname of the job
        parameters: Update the default parameters of the job.
        cluster_url: Optional URL to a specific Jenkins cluster

    Returns:
        The build number of the job
    """
    return client(ctx, cluster_url).build.build_job(fullname, parameters)


@mcp.tool()
async def get_build_logs(ctx: Context, fullname: str, build_number: str = None, cluster_url: str = None) -> str:
    """
    Get logs from a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        build_number: The number of the build
        cluster_url: Optional URL to a specific Jenkins cluster

    Returns:
        str: The logs of the build
    """
    jenkins_client = client(ctx, cluster_url)
    if build_number is None:
        build_number = jenkins_client.job.get_job_info(fullname).lastBuild.number
    return jenkins_client.build.get_build_logs(fullname, int(build_number))
