from typing import List

from sitedeployer.Projekt.Project._Project.Project import Project


class basedata_Project(
    Project
):
    def NAME(self) -> str:
        return 'basedata'
    
    def pythonanywhere_username(self) -> str:
        return 'getbasedata'

    def github_url_type(self) -> str:
        return 'ssh'

    def version_list(self) -> List[int]:
        return [2019, 2, 0]
