from sitedeployer.projects.core.Project import Project

class skfb_Project(
    Project
):
    def NAME(self) -> str:
        return 'skfb'

    def pythonanywhere_username(self) -> str:
        return 'skfb'

    def github_url_type(self) -> str:
        return 'ssh'
