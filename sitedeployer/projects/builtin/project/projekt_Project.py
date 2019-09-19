from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class projekt_Project(
    Project
):
    def NAME(self) -> str:
        return 'projekt'

    def pythonanywhere_username(self) -> str:
        return 'getprojekt'

    def github_url_type(self) -> str:
        return 'ssh'
