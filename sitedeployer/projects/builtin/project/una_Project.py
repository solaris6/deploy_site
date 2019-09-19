from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class una_Project(
    Project
):
    def NAME(self) -> str:
        return 'una'

    def pythonanywhere_username(self) -> str:
        return 'getuna'

    def github_url_type(self) -> str:
        return 'ssh'
