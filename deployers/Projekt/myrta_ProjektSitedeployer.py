from pathlib import Path
from typing import Type, List

from deployers.Projekt._Projekt_Sitedeployer import Projekt_Sitedeployer, logger


class myrta_ProjektSitedeployer(
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
        return 'myrta'
    
    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getmyrta'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies_self() -> List[Type[Projekt_Sitedeployer]]:
        from deployers.Projekt.una_ProjektSitedeployer import una_ProjektSitedeployer
        from deployers.Projekt.rs_ProjektSitedeployer import rs_ProjektSitedeployer
        from deployers.Projekt.fw_ProjektSitedeployer import fw_ProjektSitedeployer
        from deployers.Projekt.sola_ProjektSitedeployer import sola_ProjektSitedeployer
        from deployers.Projekt.Ln_ProjektSitedeployer import Ln_ProjektSitedeployer
        return [
            # una_ProjektSitedeployer,
            # rs_ProjektSitedeployer,
            # fw_ProjektSitedeployer,
            # sola_ProjektSitedeployer,
            # Ln_ProjektSitedeployer
        ]
