from pathlib import Path
from typing import List

from sitedeployer.Projekt.Project._Project.Project import Project


class myrta_Project(
    Project
):
    def NAME(self) -> str:
        return 'myrta'
    
    def pythonanywhere_username(self) -> str:
        return 'getmyrta'

    def github_url_type(self) -> str:
        return 'ssh'

    def version_list(self) -> List[int]:
        return [2019, 2, 0]

    def is_uninstall_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return [
            'myrta',
            'myrta.sh',
            'myrta.bat',
            'myrta_.py',
            'myrta.py'
        ]


    def PATHDIRS_packages_to_upload_to_testpypi(self) -> List[Path]:
        return [
            # Path('src/myrta')
        ]