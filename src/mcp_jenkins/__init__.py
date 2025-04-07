import os

import click

from .server import mcp


@click.command()
@click.option('--jenkins-url', required=True)
@click.option('--jenkins-username', required=True)
@click.option('--jenkins-password', required=True)
@click.option('--jenkins-timeout', default=5)
def main(
        jenkins_url: str,
        jenkins_username: str,
        jenkins_password: str,
        jenkins_timeout: int,
) -> None:
    """
    Jenkins' functionality for MCP
    """
    if all([jenkins_url, jenkins_username, jenkins_password, jenkins_timeout]):
        os.environ['jenkins_url'] = jenkins_url
        os.environ['jenkins_username'] = jenkins_username
        os.environ['jenkins_password'] = jenkins_password
        os.environ['jenkins_timeout'] = str(jenkins_timeout)
    else:
        raise ValueError('Please provide valid jenkins_url, jenkins_username, and jenkins_password')

    mcp.run()


if __name__ == '__main__':
    main()
