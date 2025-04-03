import pytest
from pydantic import ValidationError

from mcp_jenkins.models.job import Folder, Job, JobBase


def test_job_base_initialization():
    job = JobBase(class_='some_class', name='job_name', url='http://example.com', fullname='job_fullname')
    assert job.class_ == 'some_class'
    assert job.name == 'job_name'
    assert job.url == 'http://example.com'
    assert job.fullname == 'job_fullname'


def test_job_initialization():
    job = Job(class_='some_class', name='job_name', url='http://example.com', fullname='job_fullname', color='blue')
    assert job.color == 'blue'


def test_test_folder_initialization():
    job1 = Job(class_='some_class', name='job1', url='http://example.com/job1', fullname='job1_fullname', color='red')
    job2 = Job(class_='some_class', name='job2', url='http://example.com/job2', fullname='job2_fullname', color='green')
    folder = Folder(class_='folder_class', name='folder_name', url='http://example.com/folder',
                    fullname='folder_fullname', jobs=[job1, job2])
    assert len(folder.jobs) == 2


def test_job_base_missing_required_field():
    with pytest.raises(ValidationError):
        JobBase(name='job_name', url='http://example.com', fullname='job_fullname')


def test_folder_empty_jobs():
    folder = Folder(class_='folder_class', name='folder_name', url='http://example.com/folder',
                    fullname='folder_fullname', jobs=[])
    assert folder.jobs == []
