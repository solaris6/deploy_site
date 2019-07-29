from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Projektproject import Projektproject, logger

class base_Projektproject(
    Projektproject
):
    def NAME(self) -> str:
        return 'base'
    
    def pythonanywhere_username(self) -> str:
        return 'getbase'

    def github_url_type(self) -> str:
        return 'ssh'

    def dependencies_lib_self_Types(self) -> List[Type[Projektproject]]:
        from sitedeployer.projects.builtin.projekt.una_Projektproject import una_Projektproject
        from sitedeployer.projects.builtin.projekt.rs_Projektproject import rs_Projektproject
        from sitedeployer.projects.builtin.projekt.fw_Projektproject import fw_Projektproject
        from sitedeployer.projects.builtin.projekt.sola_Projektproject import sola_Projektproject
        from sitedeployer.projects.builtin.projekt.Ln_Projektproject import Ln_Projektproject
        return [
            # una_Projektproject,
            # rs_Projektproject,
            # fw_Projektproject,
            # sola_Projektproject,
            # Ln_Projektproject
        ]
