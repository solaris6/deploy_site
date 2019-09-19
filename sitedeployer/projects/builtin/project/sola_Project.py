from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class sola_Project(
    Project
):
    def NAME(self) -> str:
        return 'sola'

    def pythonanywhere_username(self) -> str:
        return 'getsola'

    def github_url_type(self) -> str:
        return 'ssh'
