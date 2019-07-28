from pathlib import Path
from typing import Type, List

from targets.core.Projekttarget import Projekttarget, logger

class rs_Projekttarget(
    Projekttarget
):
    def NAME(self) -> str:
        return 'rs'
    
    def pythonanywhere_username(self) -> str:
        return 'getrs'

    def github_url_type(self) -> str:
        return 'ssh'

    def ynsight_dependencies_self(self) -> List[Type[Projekttarget]]:
        from targets.builtin.projekt.una_Projekttarget import una_Projekttarget
        from targets.builtin.projekt.fw_Projekttarget import fw_Projekttarget
        from targets.builtin.projekt.sola_Projekttarget import sola_Projekttarget
        from targets.builtin.projekt.Ln_Projekttarget import Ln_Projekttarget
        return [
            una_Projekttarget,
            # rs_Projekttarget,
            # fw_Projekttarget,
            # sola_Projekttarget,
            # Ln_Projekttarget
        ]
