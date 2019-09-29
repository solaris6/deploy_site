from typing import List

from sitedeployer.Projekt.Project._Project.Project import Project


class projekt_Project(
    Project
):
    def NAME(self) -> str:
        return 'projekt'

    def pythonanywhere_username(self) -> str:
        return 'getprojekt'

    def github_url_type(self) -> str:
        return 'ssh'

    def version_list(self) -> List[int]:
        return [2019, 2, 0]


    def is_install_as_package_supported(self) -> bool:
        return True

    def is_uninstall_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return [
            'projekt',
            'projekt.sh',
            'projekt.bat',
            'projekt_.py'
        ]
