import pytest

from mcp_jenkins.models.job import Folder, Job


@pytest.fixture
def refresh_jobs(jenkins_client):
    new_jobs = [
        {
            '_class': 'com.tikal.jenkins.plugins.multijob.MultiJobProject',
            'name': 'sub_job',
            'url': 'http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            'fullname': 'main_folder/sub_folder/sub_job',
            'color': 'blue'
        }
    ]
    jenkins_client.jenkins.get_jobs.return_value = new_jobs


def test_job_to_model_returns_job(jenkins_client):
    job_data = {
        '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowJob',
        'name': 'job1',
        'url': 'http://localhost:8080/job/job1/',
        'fullname': 'job1',
        'color': 'blue'
    }
    model = jenkins_client._job_to_model(job_data)

    assert model == Job(
        class_='org.jenkinsci.plugins.workflow.job.WorkflowJob',
        name='job1',
        url='http://localhost:8080/job/job1/',
        fullname='job1',
        color='blue'
    )


def test_job_to_model_returns_folder(jenkins_client):
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
    model = jenkins_client._job_to_model(job_data)

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


def test_get_all_jobs_refresh_false(jenkins_client, refresh_jobs):
    jobs = jenkins_client.get_all_jobs(refresh=False)
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


def test_get_all_jobs_refresh_true(jenkins_client, refresh_jobs):
    jobs = jenkins_client.get_all_jobs(refresh=True)
    assert jobs == [
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_class_pattern_refresh_false(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(class_pattern='.*Folder')
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


def test_search_jobs_class_pattern_refresh_true(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(class_pattern='.*MultiJobProject', refresh=True)
    assert jobs == [
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_name_pattern_refresh_false(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(name_pattern='main_folder')
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


def test_search_jobs_name_pattern_refresh_true(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(name_pattern='main_job', refresh=True)
    assert jobs == []


def test_search_jobs_fullname_pattern_refresh_false(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(fullname_pattern='main_folder/sub_folder/')
    assert jobs == [
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_fullname_pattern_refresh_true(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(fullname_pattern='main_folder/sub_folder/', refresh=True)
    assert jobs == [
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_url_pattern_refresh_false(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(url_pattern='http://localhost:8080/job/main_folder/sub_folder/')
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


def test_search_jobs_url_pattern_refresh_true(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(url_pattern='http://localhost:8080/job/main_folder/sub_folder/', refresh=True)
    assert jobs == [
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_color_pattern_refresh_false(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(color_pattern='blue|notbuilt')
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


def test_search_jobs_color_pattern_refresh_true(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(color_pattern='blue|notbuilt', refresh=True)
    assert jobs == [
        Job(
            class_='com.tikal.jenkins.plugins.multijob.MultiJobProject',
            name='sub_job',
            url='http://localhost:8080/job/main_folder/sub_folder/sub_job/',
            fullname='main_folder/sub_folder/sub_job',
            color='blue'
        )
    ]


def test_search_jobs_combin_patterns_refresh_false(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(
        class_pattern='.*Job',
        name_pattern='.*job',
        fullname_pattern='.*sub_folder/',
        url_pattern='.*main_folder',
        color_pattern='blue|notbuilt',
        refresh=True
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


def test_search_jobs_combin_patterns_refresh_true(jenkins_client, refresh_jobs):
    jobs = jenkins_client.search_jobs(
        class_pattern='.*Job',
        name_pattern='.*main',
        fullname_pattern='.*sub_folder/',
        url_pattern='.*main_folder',
        color_pattern='blue|notbuilt',
        refresh=True
    )

    assert jobs == []


def test_job_config(jenkins_client):
    config = jenkins_client.get_job_config('main_folder/main_job')
    assert config == ''
