from jenkins import Jenkins

from mcp_jenkins.models.build import Build


class JenkinsBuild:
    def __init__(self, jenkins: Jenkins) -> None:
        self.jenkins = jenkins

    @staticmethod
    def _to_model(data: dict) -> Build:
        return Build.model_validate(data)

    def get_running_builds(self) -> list[Build]:
        builds = self.jenkins.get_running_builds()
        return [self._to_model(build) for build in builds]
