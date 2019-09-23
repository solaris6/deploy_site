from sitedeployer.projects.core.Project import Project

class basedata_Project(
    Project
):
    def NAME(self) -> str:
        return 'basedata'
    
    def pythonanywhere_username(self) -> str:
        return 'getbasedata'

    def github_url_type(self) -> str:
        return 'ssh'
