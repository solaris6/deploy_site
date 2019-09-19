from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class base_Project(
    Project
):
    def NAME(self) -> str:
        return 'base'
    
    def pythonanywhere_username(self) -> str:
        return 'getbase'

    def github_url_type(self) -> str:
        return 'ssh'
