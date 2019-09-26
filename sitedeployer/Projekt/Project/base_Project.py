from typing import List

from sitedeployer.Projekt.Project._Project.Project import Project


class base_Project(
    Project
):
    def NAME(self) -> str:
        return 'base'
    
    def pythonanywhere_username(self) -> str:
        return 'getbase'

    def github_url_type(self) -> str:
        return 'ssh'

    def version_list(self) -> List[int]:
        return [2019, 2, 0]


    def is_install_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return [
            'agent',
            'agent.sh',
            'agent.bat',
            'agent.py',

            'deck',
            'deck.sh',
            'deck.bat',
            'deck.py',

            'base',
            'base.sh',
            'base.bat',
            'base.py'
        ]