from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class cgbase_Project(
    Project
):
    def NAME(self) -> str:
        return 'cgbase'

    def pythonanywhere_username(self) -> str:
        return 'getcgbase'

    def github_url_type(self) -> str:
        return 'ssh'