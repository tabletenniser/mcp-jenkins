from uuid import uuid4

from jenkins import Jenkins

from mcp_jenkins.models.build import Build


class JenkinsBuild:
    def __init__(self, jenkins: Jenkins) -> None:
        self._jenkins = jenkins

    @staticmethod
    def _to_model(data: dict) -> Build:
        return Build.model_validate(data)

    def get_running_builds(self) -> list[Build]:
        builds = self._jenkins.get_running_builds()
        return [self._to_model(build) for build in builds]

    def get_build_info(self, fullname: str, number: int) -> Build:
        return self._to_model(self._jenkins.get_build_info(fullname, number))

    def build_job(self, fullname: str, parameters: dict | None = None) -> int:
        # In jenkins lib, {} is same as None, so I need to mock a foo param to make it work
        foo = str(uuid4())
        parameters = {foo: foo} if parameters == {} else parameters

        return self._jenkins.build_job(fullname, parameters)
