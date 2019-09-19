from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project, logger

class rs_Project(
    Project
):
    def NAME(self) -> str:
        return 'rs'
    
    def pythonanywhere_username(self) -> str:
        return 'getrs'

    def github_url_type(self) -> str:
        return 'ssh'
