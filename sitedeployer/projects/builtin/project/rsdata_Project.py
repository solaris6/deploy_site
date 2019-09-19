from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class rsdata_Project(
    Project
):
    def NAME(self) -> str:
        return 'rsdata'
    
    def pythonanywhere_username(self) -> str:
        return 'getrsdata'

    def github_url_type(self) -> str:
        return 'ssh'
