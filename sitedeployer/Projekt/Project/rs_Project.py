from pathlib import Path
from typing import List

from sitedeployer.Projekt.Project._Project.Project import Project


class rs_Project(
    Project
):
    def NAME(self) -> str:
        return 'rs'
    
    def pythonanywhere_username(self) -> str:
        return 'getrs'

    def github_url_type(self) -> str:
        return 'ssh'

    def is_uninstall_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return []
