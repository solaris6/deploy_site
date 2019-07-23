from pathlib import Path
from typing import Type, List

from deployers.Projekt._Projekt_Sitedeployer import Projekt_Sitedeployer
from deployers.Workshop._Workshop_Sitedeployer import Workshop_Sitedeployer, logger


# ynsight:
class ynsight_WorkshopSitedeployer(
    Workshop_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Workshop_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'ynsight'

    @staticmethod
    def pythonanywhere_username() -> str:
        return 'ynsight'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_projekts() -> List[Type[Projekt_Sitedeployer]]:
        from deployers.Projekt.base_ProjektSitedeployer import base_ProjektSitedeployer
        from deployers.Projekt.projekt_ProjektSitedeployer import projekt_ProjektSitedeployer
        from deployers.Projekt.myrta_ProjektSitedeployer import myrta_ProjektSitedeployer
        from deployers.Projekt.una_ProjektSitedeployer import una_ProjektSitedeployer
        from deployers.Projekt.rs_ProjektSitedeployer import rs_ProjektSitedeployer
        from deployers.Projekt.fw_ProjektSitedeployer import fw_ProjektSitedeployer
        from deployers.Projekt.sola_ProjektSitedeployer import sola_ProjektSitedeployer
        from deployers.Projekt.Ln_ProjektSitedeployer import Ln_ProjektSitedeployer
        return [
            base_ProjektSitedeployer,
            projekt_ProjektSitedeployer,
            myrta_ProjektSitedeployer,
            una_ProjektSitedeployer,
            rs_ProjektSitedeployer,
            fw_ProjektSitedeployer,
            sola_ProjektSitedeployer,
            Ln_ProjektSitedeployer
        ]

    @staticmethod
    def ynsight_dependencies() -> List[Type[Projekt_Sitedeployer]]:
        from deployers.Projekt.base_ProjektSitedeployer import base_ProjektSitedeployer
        from deployers.Projekt.projekt_ProjektSitedeployer import projekt_ProjektSitedeployer
        from deployers.Projekt.myrta_ProjektSitedeployer import myrta_ProjektSitedeployer
        from deployers.Projekt.una_ProjektSitedeployer import una_ProjektSitedeployer
        from deployers.Projekt.rs_ProjektSitedeployer import rs_ProjektSitedeployer
        from deployers.Projekt.fw_ProjektSitedeployer import fw_ProjektSitedeployer
        from deployers.Projekt.sola_ProjektSitedeployer import sola_ProjektSitedeployer
        from deployers.Projekt.Ln_ProjektSitedeployer import Ln_ProjektSitedeployer
        return [
            base_ProjektSitedeployer,
            projekt_ProjektSitedeployer,
            myrta_ProjektSitedeployer,
            una_ProjektSitedeployer,
            rs_ProjektSitedeployer,
            fw_ProjektSitedeployer,
            # sola_ProjektSitedeployer,
            # Ln_ProjektSitedeployer
        ]
