from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class fw_Project(
    Project
):
    def NAME(self) -> str:
        return 'fw'
    
    def pythonanywhere_username(self) -> str:
        return 'getfw'

    def github_url_type(self) -> str:
        return 'ssh'
