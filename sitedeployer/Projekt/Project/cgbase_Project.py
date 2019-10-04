from typing import List

from sitedeployer.Projekt.Project._Project.Project import Project


class cgbase_Project(
    Project
):
    def NAME(self) -> str:
        return 'cgbase'

    def pythonanywhere_username(self) -> str:
        return 'getcgbase'

    def github_url_type(self) -> str:
        return 'ssh'

    def version_list(self) -> List[int]:
        return [2019, 2, 0]

    def is_uninstall_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return []
