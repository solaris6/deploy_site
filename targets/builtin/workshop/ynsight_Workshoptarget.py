from pathlib import Path
from typing import Type, List

from targets.core.Projekttarget import Projekttarget
from targets.core.Workshoptarget import Workshoptarget, logger

:
class ynsight_Workshoptarget(
    Workshoptarget
):
    def NAME(self) -> str:
        return 'ynsight'

    def pythonanywhere_username(self) -> str:
        return 'ynsight'

    def github_url_type(self) -> str:
        return 'ssh'

    def workshop_projects(self) -> List[Type[Projekttarget]]:
        from targets.builtin.projekt.base_Projekttarget import base_Projekttarget
        from targets.builtin.projekt.projekt_Projekttarget import projekt_Projekttarget
        from targets.builtin.projekt.myrta_Projekttarget import myrta_Projekttarget
        from targets.builtin.projekt.una_Projekttarget import una_Projekttarget
        from targets.builtin.projekt.rs_Projekttarget import rs_Projekttarget
        from targets.builtin.projekt.fw_Projekttarget import fw_Projekttarget
        from targets.builtin.projekt.sola_Projekttarget import sola_Projekttarget
        from targets.builtin.projekt.Ln_Projekttarget import Ln_Projekttarget
        return [
            base_Projekttarget,
            projekt_Projekttarget,
            myrta_Projekttarget,
            una_Projekttarget,
            rs_Projekttarget,
            fw_Projekttarget,
            sola_Projekttarget,
            Ln_Projekttarget
        ]

    def ynsight_dependencies_self(self) -> List[Type[Projekttarget]]:
        from targets.builtin.projekt.una_Projekttarget import una_Projekttarget
        from targets.builtin.projekt.rs_Projekttarget import rs_Projekttarget
        from targets.builtin.projekt.fw_Projekttarget import fw_Projekttarget
        from targets.builtin.projekt.sola_Projekttarget import sola_Projekttarget
        from targets.builtin.projekt.Ln_Projekttarget import Ln_Projekttarget
        return [
            una_Projekttarget,
            rs_Projekttarget,
            fw_Projekttarget,
            # sola_Projekttarget,
            # Ln_Projekttarget
        ]
