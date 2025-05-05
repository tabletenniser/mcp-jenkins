import os

import click

from mcp_jenkins.server import mcp


@click.command()
@click.option('--jenkins-url', required=True)
@click.option('--jenkins-username', required=True)
@click.option('--jenkins-password', required=True)
@click.option('--jenkins-timeout', default=5)
@click.option('--transport', type=click.Choice(['stdio', 'sse']), default='stdio')
@click.option('--port', default=9887, help='Port to listen on for SSE transport')
def main(
    jenkins_url: str,
    jenkins_username: str,
    jenkins_password: str,
    jenkins_timeout: int,
    transport: str,
    port: int,
) -> None:
    """
    Jenkins' functionality for MCP
    """
    # Split the comma-separated values
    jenkins_urls = jenkins_url.split(',')
    jenkins_usernames = jenkins_username.split(',')
    jenkins_passwords = jenkins_password.split(',')

    # Ensure all lists have the same length or handle different lengths appropriately
    count = max(len(jenkins_urls), len(jenkins_usernames), len(jenkins_passwords))

    # Extend shorter lists by repeating the last element
    if len(jenkins_urls) < count:
        jenkins_urls.extend([jenkins_urls[-1]] * (count - len(jenkins_urls)))
    if len(jenkins_usernames) < count:
        jenkins_usernames.extend([jenkins_usernames[-1]] * (count - len(jenkins_usernames)))
    if len(jenkins_passwords) < count:
        jenkins_passwords.extend([jenkins_passwords[-1]] * (count - len(jenkins_passwords)))

    # Store the configurations
    if all([jenkins_urls, jenkins_usernames, jenkins_passwords]):
        # Store the count of Jenkins instances
        os.environ['jenkins_count'] = str(count)

        for i, (url, username, password) in enumerate(
            zip(jenkins_urls, jenkins_usernames, jenkins_passwords, strict=False)
        ):
            os.environ[f'jenkins_url_{i}'] = url
            os.environ[f'jenkins_username_{i}'] = username
            os.environ[f'jenkins_password_{i}'] = password
            os.environ[f'jenkins_timeout_{i}'] = str(jenkins_timeout)
    else:
        raise ValueError('Please provide valid jenkins_url, jenkins_username, and jenkins_password')

    if transport == 'sse':
        mcp.settings.port = port
    mcp.run(transport=transport)


if __name__ == '__main__':
    main()
