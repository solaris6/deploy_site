from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class sc_Project(
    Project
):
    def NAME(self) -> str:
        return 'sc'
    
    def pythonanywhere_username(self) -> str:
        return 'getsc'

    def github_url_type(self) -> str:
        return 'ssh'
