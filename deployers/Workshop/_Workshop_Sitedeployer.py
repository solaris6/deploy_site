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
    def workshop_projekts() -> List[Type[Projekt_Sitedeployer]]:
        raise NotImplementedError("")

    @classmethod
    def ynsight_dependencies(cls) -> List[Type[Projekt_Sitedeployer]]:
        return Sitedeployer.ynsight_dependencies() + cls.workshop_projekts()


    def Execute(self) -> None:
        pass
