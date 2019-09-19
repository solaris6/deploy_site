from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class myrta_Project(
    Project
):
    def NAME(self) -> str:
        return 'myrta'
    
    def pythonanywhere_username(self) -> str:
        return 'getmyrta'

    def github_url_type(self) -> str:
        return 'ssh'
