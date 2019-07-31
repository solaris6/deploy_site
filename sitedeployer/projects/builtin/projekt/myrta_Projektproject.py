from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Projektproject import Projektproject, logger

class myrta_Projektproject(
    Projektproject
):
    def NAME(self) -> str:
        return 'myrta'
    
    def pythonanywhere_username(self) -> str:
        return 'getmyrta'

    def github_url_type(self) -> str:
        return 'ssh'

    def dependencies_lib_temp_Types(self) -> List[Type[Projektproject]]:
        from sitedeployer.projects.builtin.projekt.base_Projektproject import base_Projektproject
        from sitedeployer.projects.builtin.projekt.projekt_Projektproject import projekt_Projektproject
        return [
            base_Projektproject,
            projekt_Projektproject,
            myrta_Projektproject
        ]

    def dependencies_lib_deployer_Types(self) -> List[Type[Projektproject]]:
        from sitedeployer.projects.builtin.projekt.base_Projektproject import base_Projektproject
        from sitedeployer.projects.builtin.projekt.projekt_Projektproject import projekt_Projektproject
        return [
            base_Projektproject,
            projekt_Projektproject,
            myrta_Projektproject
        ]

    def dependencies_lib_site_Types(self) -> List[Type[Projektproject]]:
        from sitedeployer.projects.builtin.projekt.base_Projektproject import base_Projektproject
        from sitedeployer.projects.builtin.projekt.projekt_Projektproject import projekt_Projektproject
        return [
            base_Projektproject,
            projekt_Projektproject,
            myrta_Projektproject
        ]
