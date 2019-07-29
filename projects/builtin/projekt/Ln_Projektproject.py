from pathlib import Path
from typing import Type, List

from projects.core.Projektproject import Projektproject, logger

class Ln_Projektproject(
    Projektproject
):
    def NAME(self) -> str:
        return 'Ln'
    
    def pythonanywhere_username(self) -> str:
        return 'getln'

    def github_url_type(self) -> str:
        return 'ssh'

    def dependencies_lib_Types(self) -> List[Type[Projektproject]]:
        from projects.builtin.projekt.una_Projektproject import una_Projektproject
        from projects.builtin.projekt.rs_Projektproject import rs_Projektproject
        from projects.builtin.projekt.fw_Projektproject import fw_Projektproject
        from projects.builtin.projekt.sola_Projektproject import sola_Projektproject
        return [
            una_Projektproject,
            # rs_Projektproject,
            fw_Projektproject,
            # sola_Projektproject,
            # Ln_Projektproject
        ]
