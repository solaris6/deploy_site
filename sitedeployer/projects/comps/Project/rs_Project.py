from sitedeployer.projects.core.Project import Project

class rs_Project(
    Project
):
    def NAME(self) -> str:
        return 'rs'
    
    def pythonanywhere_username(self) -> str:
        return 'getrs'

    def github_url_type(self) -> str:
        return 'ssh'
