from unittest.mock import MagicMock, patch

import pytest

from mcp_jenkins.jenkins import JenkinsClient

JOBS = [
    {
        '_class': 'com.cloudbees.hudson.plugins.folder.Folder',
        'name': 'main_folder',
        'url': 'http://localhost:8080/job/main_folder/',
        'fullname': 'main_folder',
        'jobs': [
            {
                '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowJob',
                'name': 'main_job',
                'url': 'http://localhost:8080/job/main_folder/main_job/',
                'fullname': 'main_folder/main_job',
                'color': 'notbuilt'
            },
            {
                '_class': 'com.cloudbees.hudson.plugins.folder.Folder',
                'name': 'sub_folder',
                'url': 'http://localhost:8080/job/main_folder/sub_folder/',
                'fullname': 'main_folder/sub_folder',
                'jobs': [
                    {
                        '_class': 'com.tikal.jenkins.plugins.multijob.MultiJobProject',
                        'name': 'sub_job',
                        'url': 'http://localhost:8080/job/main_folder/sub_folder/sub_job/',
                        'fullname': 'main_folder/sub_folder/sub_job',
                        'color': 'blue'
                    }
                ]
            }
        ]
    },
    {
        '_class': 'com.cloudbees.hudson.plugins.folder.Folder',
        'name': 'sub_folder',
        'url': 'http://localhost:8080/job/main_folder/sub_folder/',
        'fullname': 'main_folder/sub_folder',
        'jobs': [
            {
                '_class': 'com.tikal.jenkins.plugins.multijob.MultiJobProject',
                'name': 'sub_job',
                'url': 'http://localhost:8080/job/main_folder/sub_folder/sub_job/',
                'fullname': 'main_folder/sub_folder/sub_job',
                'color': 'blue'
            }
        ]
    },
    {
        '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowJob',
        'name': 'main_job',
        'url': 'http://localhost:8080/job/main_folder/main_job/',
        'fullname': 'main_folder/main_job',
        'color': 'notbuilt'
    },
    {
        '_class': 'com.tikal.jenkins.plugins.multijob.MultiJobProject',
        'name': 'sub_job',
        'url': 'http://localhost:8080/job/main_folder/sub_folder/sub_job/',
        'fullname': 'main_folder/sub_folder/sub_job',
        'color': 'blue'
    }
]


@pytest.fixture
def mock_jenkins_config():
    return {
        "username": "test_user",
        "password": "test_password",
        "url": "http://localhost:8080",
    }


@pytest.fixture
def mock_jenkins():
    mock_jenkins = MagicMock()

    mock_jenkins.get_jobs.return_value = JOBS.copy()
    mock_jenkins.get_job_config.return_value = ''

    yield mock_jenkins

    mock_jenkins.get_jobs.return_value = JOBS.copy()


@pytest.fixture
def jenkins_client(mock_jenkins, mock_jenkins_config):
    with patch('mcp_jenkins.jenkins.JenkinsClient.__init__', return_value=None):
        client = JenkinsClient(**mock_jenkins_config)
        client.jenkins = mock_jenkins
        client.jobs = client.get_all_jobs(refresh=True)

        yield client
