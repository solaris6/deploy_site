from pathlib import Path
from typing import Type, List

from deployers.core.Projekt_Sitedeployer import Projekt_Sitedeployer, logger

class fw_ProjektSitedeployer(
    Projekt_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Projekt_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'fw'
    
    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getfw'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies_self() -> List[Type[Projekt_Sitedeployer]]:
        from deployers.builtin.projekt.una_ProjektSitedeployer import una_ProjektSitedeployer
        from deployers.builtin.projekt.rs_ProjektSitedeployer import rs_ProjektSitedeployer
        from deployers.builtin.projekt.sola_ProjektSitedeployer import sola_ProjektSitedeployer
        from deployers.builtin.projekt.Ln_ProjektSitedeployer import Ln_ProjektSitedeployer
        return [
            una_ProjektSitedeployer,
            # rs_ProjektSitedeployer,
            # fw_ProjektSitedeployer,
            # sola_ProjektSitedeployer,
            # Ln_ProjektSitedeployer
        ]
