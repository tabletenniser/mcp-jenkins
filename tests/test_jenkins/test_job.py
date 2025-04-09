import pytest

from mcp_jenkins.jenkins._job import JenkinsJob
from mcp_jenkins.models.build import Build
from mcp_jenkins.models.job import Folder, Job

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

JOB_INFO = {
    '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowJob',
    'fullName': 'folder/job',
    'name': 'job',
    'url': 'http://localhost:8080/job/folder/job/job/',
    'buildable': True,
    'builds': [
        {
            '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowRun',
            'number': 110,
            'url': 'http://localhost:8080/job/folder/job/job/110'
        }
    ],
    'color': 'blue',
    'lastBuild': {
        '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowRun',
        'number': 110,
        'url': 'http://localhost:8080/job/folder/job/job/110'
    },
    'nextBuildNumber': 111,
    'inQueue': False,
}

FOLDER_INFO = {
    '_class': 'com.cloudbees.hudson.plugins.folder.Folder',
    'fullName': 'folder',
    'name': 'folder',
    'url': 'http://localhost:8080/job/folder/',
    'jobs': [
        {
            '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowJob',
            'name': 'job',
            'url': 'http://localhost:8080/job/folder/job/job/',
            'color': 'blue'
        },
    ]
}


@pytest.fixture()
def jenkins_job(mock_jenkins):
    mock_jenkins.get_jobs.return_value = JOBS
    mock_jenkins.get_job_info.return_value = JOB_INFO
    mock_jenkins.get_job_config.return_value = ''

    yield JenkinsJob(mock_jenkins)

    mock_jenkins.get_jobs.return_value = JOBS
    mock_jenkins.get_job_info.return_value = JOB_INFO
    mock_jenkins.get_job_config.return_value = ''


def test_to_model_returns_job(jenkins_job):
    job_data = {
        '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowJob',
        'name': 'job1',
        'url': 'http://localhost:8080/job/job1/',
        'fullname': 'job1',
        'color': 'blue'
    }
    model = jenkins_job._to_model(job_data)

    assert model == Job(
        class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
        name='job1',
        url='http://localhost:8080/job/job1/',
        fullname='job1',
        color='blue'
    )


def test_to_model_returns_folder(jenkins_job):
    job_data = {
        '_class': 'com.cloudbees.hudson.plugins.folder.Folder',
        'name': 'folder1',
        'url': 'http://localhost:8080/job/folder1/',
        'fullname': 'folder1',
        'jobs': [
            {
                '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowJob',
                'name': 'job1',
                'url': 'http://localhost:8080/job/folder1/job1/',
                'fullname': 'folder1/job1',
                'color': 'blue'
            }
        ]
    }
    model = jenkins_job._to_model(job_data)

    assert model == Folder(
        class_='com.cloudbees.hudson.plugins.folder.Folder',
        name='folder1',
        url='http://localhost:8080/job/folder1/',
        fullname='folder1',
        jobs=[
            Job(
                class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
                name='job1',
                url='http://localhost:8080/job/folder1/job1/',
                fullname='folder1/job1',
                color='blue'
            )
        ]
    )


def test_get_all_jobs(jenkins_job):
    jobs = jenkins_job.get_all_jobs()
    assert jobs == [
        Folder(
            class_='com.cloudbees.hudson.plugins.folder.Folder',
            name='main_folder',
            url='http://localhost:8080/job/main_folder/',
            fullname='main_folder',
            jobs=[
                Job(
                    class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
                    name='main_job',
                    url='http://localhost:8080/job/main_folder/main_job/',
                    fullname='main_folder/main_job',
                    color='notbuilt'
                ),
                Folder(
                    class_='com.cloudbees.hudson.plugins.folder.Folder',
                    name='sub_folder',
                    url='http://localhost:8080/job/main_folder/sub_folder/',
                    fullname='main_folder/sub_folder',
                    jobs=[
                        Job(
                            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
                            name='sub_job',
                            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
                            fullname='main_folder/sub_folder/sub_job',
                            color='blue'
                        )
                    ]
                )
            ]
        ),
        Folder(
            class_='com.cloudbees.hudson.plugins.folder.Folder',
            name='sub_folder',
            url='http://localhost:8080/job/main_folder/sub_folder/',
            fullname='main_folder/sub_folder',
            jobs=[
                Job(
                    class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
                    name='sub_job',
                    url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
                    fullname='main_folder/sub_folder/sub_job',
                    color='blue'
                )
            ]
        ),
        Job(
            class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
            name='main_job',
            url='http://localhost:8080/job/main_folder/main_job/',
            fullname='main_folder/main_job',
            color='notbuilt'
        ),
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_class_pattern(jenkins_job):
    jobs = jenkins_job.search_jobs(class_pattern='.*Folder')
    assert jobs == [
        Folder(
            class_='com.cloudbees.hudson.plugins.folder.Folder',
            name='main_folder',
            url='http://localhost:8080/job/main_folder/',
            fullname='main_folder',
            jobs=[
                Job(
                    class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
                    name='main_job',
                    url='http://localhost:8080/job/main_folder/main_job/',
                    fullname='main_folder/main_job',
                    color='notbuilt'
                ),
                Folder(
                    class_='com.cloudbees.hudson.plugins.folder.Folder',
                    name='sub_folder',
                    url='http://localhost:8080/job/main_folder/sub_folder/',
                    fullname='main_folder/sub_folder',
                    jobs=[
                        Job(
                            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
                            name='sub_job',
                            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
                            fullname='main_folder/sub_folder/sub_job',
                            color='blue'
                        )
                    ]
                )
            ]
        ),
        Folder(
            class_='com.cloudbees.hudson.plugins.folder.Folder',
            name='sub_folder',
            url='http://localhost:8080/job/main_folder/sub_folder/',
            fullname='main_folder/sub_folder',
            jobs=[
                Job(
                    class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
                    name='sub_job',
                    url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
                    fullname='main_folder/sub_folder/sub_job',
                    color='blue'
                )
            ]
        )
    ]


def test_search_jobs_name_pattern(jenkins_job):
    jobs = jenkins_job.search_jobs(name_pattern='main_folder')
    assert jobs == [
        Folder(
            class_='com.cloudbees.hudson.plugins.folder.Folder',
            name='main_folder',
            url='http://localhost:8080/job/main_folder/',
            fullname='main_folder',
            jobs=[
                Job(
                    class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
                    name='main_job',
                    url='http://localhost:8080/job/main_folder/main_job/',
                    fullname='main_folder/main_job',
                    color='notbuilt'
                ),
                Folder(
                    class_='com.cloudbees.hudson.plugins.folder.Folder',
                    name='sub_folder',
                    url='http://localhost:8080/job/main_folder/sub_folder/',
                    fullname='main_folder/sub_folder',
                    jobs=[
                        Job(
                            _class='com.tikal.jenkins.plugins.multijob.MultiJobProject',
                            name='sub_job',
                            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
                            fullname='main_folder/sub_folder/sub_job',
                            color='blue'
                        )
                    ]
                )
            ]
        )
    ]


def test_search_jobs_fullname_pattern(jenkins_job):
    jobs = jenkins_job.search_jobs(fullname_pattern='main_folder/sub_folder/')
    assert jobs == [
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_url_pattern(jenkins_job):
    jobs = jenkins_job.search_jobs(url_pattern='http://localhost:8080/job/main_folder/sub_folder/')
    assert jobs == [
        Folder(
            class_='com.cloudbees.hudson.plugins.folder.Folder',
            name='sub_folder',
            url='http://localhost:8080/job/main_folder/sub_folder/',
            fullname='main_folder/sub_folder',
            jobs=[
                Job(
                    class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
                    name='sub_job',
                    url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
                    fullname='main_folder/sub_folder/sub_job',
                    color='blue'
                )
            ]
        ),
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_color_pattern(jenkins_job):
    jobs = jenkins_job.search_jobs(color_pattern='blue|notbuilt')
    assert jobs == [
        Job(
            class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
            name='main_job',
            url='http://localhost:8080/job/main_folder/main_job/',
            fullname='main_folder/main_job',
            color='notbuilt'
        ),
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_combin_patterns(jenkins_job):
    jobs = jenkins_job.search_jobs(
        class_pattern='.*Job',
        name_pattern='.*job',
        fullname_pattern='.*sub_folder/',
        url_pattern='.*main_folder',
        color_pattern='blue|notbuilt',
    )

    assert jobs == [
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_job_config(jenkins_job):
    config = jenkins_job.get_job_config('main_folder/main_job')
    assert config == ''


def test_get_job_info_return_job(jenkins_job):
    job_info = jenkins_job.get_job_info('folder/job')

    assert job_info == Job(
        class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
        fullName='folder/job',
        name='job',
        url='http://localhost:8080/job/folder/job/job/',
        buildable=True,
        builds=[
            Build(
                class_='org.jenkinsci.plugins.workflow.job.WorkflowRun',
                number=110,
                url='http://localhost:8080/job/folder/job/job/110'
            )
        ],
        color='blue',
        lastBuild=Build(
            class_='org.jenkinsci.plugins.workflow.job.WorkflowRun',
            number=110,
            url='http://localhost:8080/job/folder/job/job/110'
        ),
        nextBuildNumber=111,
        inQueue=False
    )


def test_get_job_info_return_folder(jenkins_job):
    jenkins_job._jenkins.get_job_info.return_value = FOLDER_INFO
    job_info = jenkins_job.get_job_info('folder')

    assert job_info == Folder(
        class_='com.cloudbees.hudson.plugins.folder.Folder',
        fullName='folder',
        name='folder',
        url='http://localhost:8080/job/folder/',
        jobs=[
            Job(
                class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
                name='job',
                url='http://localhost:8080/job/folder/job/job/',
                color='blue'
            )
        ]
    )
