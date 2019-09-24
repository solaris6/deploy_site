from typing import List

from sitedeployer.Projekt.Project._Project.Project import Project


class sola_Project(
    Project
):
    def NAME(self) -> str:
        return 'sola'

    def pythonanywhere_username(self) -> str:
        return 'getsola'

    def github_url_type(self) -> str:
        return 'ssh'

    def version_list(self) -> List[int]:
        return [2019, 2, 0]
