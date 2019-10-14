from pathlib import Path
from typing import List

from sitedeployer.Projekt.Project._Project.Project import Project

import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[sitedeployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class base_Project(
    Project
):
    def NAME(self) -> str:
        return 'base'
    
    def pythonanywhere_username(self) -> str:
        return 'getbase'

    def github_url_type(self) -> str:
        return 'ssh'

    def version_list(self) -> List[int]:
        return [2019, 2, 0]

    def is_uninstall_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return [
            'agent',
            'agent.sh',
            'agent.bat',
            'agent_.py',
            'agent.py',

            'base',
            'base.sh',
            'base.bat',
            'base_.py',
            'base.py',

            'deck',
            'deck.sh',
            'deck.bat',
            'deck_.py',
            'deck.py'
        ]


    def PATHDIRS_packages_to_upload_on_testpypi(self) -> List[Path]:
        return [
            Path('src/base')
        ]