from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class Ln_Project(
    Project
):
    def NAME(self) -> str:
        return 'Ln'
    
    def pythonanywhere_username(self) -> str:
        return 'getln'

    def github_url_type(self) -> str:
        return 'ssh'
