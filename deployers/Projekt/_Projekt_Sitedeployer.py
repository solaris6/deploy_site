from pathlib import Path

from deployers._Sitedeployer.Sitedeployer import Sitedeployer, logger


class Projekt_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def projektorworkshop_Type() -> str:
        return 'projekt'
