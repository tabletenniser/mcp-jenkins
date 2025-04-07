import pytest

from mcp_jenkins.jenkins._build import JenkinsBuild
from mcp_jenkins.models.build import Build

RUNNING_BUILDS = [
    {
        'name': 'RUN_JOB_LIST',
        'number': 2,
        'url': 'http://example.com/job/RUN_JOB_LIST/job/job-one/2/',
        'node': '(master)',
        'executor': 4
    },
    {
        'name': 'weekly',
        'number': 39,
        'url': 'http://example.com/job/weekly/job/folder-one/job/job-two/39/',
        'node': '001',
        'executor': 0
    }
]


@pytest.fixture()
def jenkins_build_client(jenkins_client):
    jenkins_client.build = JenkinsBuild(jenkins_client.jenkins)
    jenkins_client.jenkins.get_running_builds.return_value = RUNNING_BUILDS
    yield jenkins_client


def test_to_model(jenkins_build_client):
    model = jenkins_build_client.build._to_model({
        'name': 'RUN_JOB_LIST',
        'number': 2,
        'url': 'http://example.com/job/RUN_JOB_LIST/job/job-one/2/',
        'node': '(master)',
        'executor': 4
    })

    assert model == Build(
        name='RUN_JOB_LIST',
        number=2,
        url='http://example.com/job/RUN_JOB_LIST/job/job-one/2/',
        node='(master)',
        executor=4
    )


def test_get_running_builds(jenkins_build_client):
    builds = jenkins_build_client.build.get_running_builds()

    assert len(builds) == 2
    assert builds[0] == Build(
        name='RUN_JOB_LIST',
        number=2,
        url='http://example.com/job/RUN_JOB_LIST/job/job-one/2/',
        node='(master)',
        executor=4
    )
    assert builds[1] == Build(
        name='weekly',
        number=39,
        url='http://example.com/job/weekly/job/folder-one/job/job-two/39/',
        node='001',
        executor=0
    )
