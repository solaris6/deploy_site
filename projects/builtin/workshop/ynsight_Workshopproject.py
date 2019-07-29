from pathlib import Path
from typing import Type, List

from projects.core.Projektproject import Projektproject
from projects.core.Workshopproject import Workshopproject, logger


class ynsight_Workshopproject(
    Workshopproject
):
    def NAME(self) -> str:
        return 'ynsight'

    def pythonanywhere_username(self) -> str:
        return 'ynsight'

    def github_url_type(self) -> str:
        return 'ssh'

    def dependencies_workshop_Types(self) -> List[Type[Projektproject]]:
        from projects.builtin.projekt.base_Projektproject import base_Projektproject
        from projects.builtin.projekt.projekt_Projektproject import projekt_Projektproject
        from projects.builtin.projekt.myrta_Projektproject import myrta_Projektproject
        from projects.builtin.projekt.una_Projektproject import una_Projektproject
        from projects.builtin.projekt.rs_Projektproject import rs_Projektproject
        from projects.builtin.projekt.fw_Projektproject import fw_Projektproject
        from projects.builtin.projekt.sola_Projektproject import sola_Projektproject
        from projects.builtin.projekt.Ln_Projektproject import Ln_Projektproject
        return [
            base_Projektproject,
            projekt_Projektproject,
            myrta_Projektproject,
            una_Projektproject,
            rs_Projektproject,
            fw_Projektproject,
            sola_Projektproject,
            Ln_Projektproject
        ]

    def dependencies_lib_Types(self) -> List[Type[Projektproject]]:
        from projects.builtin.projekt.una_Projektproject import una_Projektproject
        from projects.builtin.projekt.rs_Projektproject import rs_Projektproject
        from projects.builtin.projekt.fw_Projektproject import fw_Projektproject
        from projects.builtin.projekt.sola_Projektproject import sola_Projektproject
        from projects.builtin.projekt.Ln_Projektproject import Ln_Projektproject
        return [
            una_Projektproject,
            rs_Projektproject,
            fw_Projektproject,
            # sola_Projektproject,
            # Ln_Projektproject
        ]
