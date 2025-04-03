import re

from jenkins import Jenkins

from mcp_jenkins.models.job import Folder, Job, JobBase


class JenkinsClient:
    def __init__(self, *, url: str, username: str, password: str, timeout: int = 5) -> None:
        self.jenkins = Jenkins(url=url, username=username, password=password, timeout=timeout)
        self.jobs = self.get_all_jobs(refresh=True)

    def _job_to_model(self, job_data: dict) -> JobBase:
        if job_data['_class'].endswith('Folder'):
            return Folder.model_validate(job_data)
        return Job.model_validate(job_data)

    def get_all_jobs(self, refresh: bool = False) -> list[JobBase]:
        if refresh:
            self.jobs = [self._job_to_model(job) for job in self.jenkins.get_jobs(folder_depth=20)]
        return self.jobs

    def search_jobs(
            self,
            class_pattern: str = None,
            name_pattern: str = None,
            fullname_pattern: str = None,
            url_pattern: str = None,
            color_pattern: str = None,
            refresh: bool = False
    ) -> list[JobBase]:
        result = []

        jobs = self.get_all_jobs(refresh=refresh)

        class_pattern = re.compile(class_pattern) if class_pattern else None
        name_pattern = re.compile(name_pattern) if name_pattern else None
        fullname_pattern = re.compile(fullname_pattern) if fullname_pattern else None
        url_pattern = re.compile(url_pattern) if url_pattern else None
        color_pattern = re.compile(color_pattern) if color_pattern else None

        for job in jobs:
            if class_pattern and not class_pattern.match(job.class_):
                continue
            if name_pattern and not name_pattern.match(job.name):
                continue
            if fullname_pattern and not fullname_pattern.match(job.fullname):
                continue
            if url_pattern and not url_pattern.match(job.url):
                continue
            # Folder do not have attribute color
            if color_pattern and (isinstance(job, Folder) or not color_pattern.match(job.color)):
                continue
            result.append(job)

        return result

    def get_job_config(self, fullname: str) -> str:
        return self.jenkins.get_job_config(fullname)
