from pathlib import Path
from typing import Type, List

from deployers.Projekt._Projekt_Sitedeployer import Projekt_Sitedeployer
from deployers._Sitedeployer.Sitedeployer import Sitedeployer, logger



class Workshop_Sitedeployer(
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
        return 'workshop'

    @staticmethod
    def projekts() -> List[Type[Projekt_Sitedeployer]]:
        raise NotImplementedError("")
