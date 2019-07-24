from pathlib import Path
from typing import Type, List

from deployers.core.Projekt_Sitedeployer import Projekt_Sitedeployer
from deployers.core.Sitedeployer import Sitedeployer, logger



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
    def workshop_projects() -> List[Type[Projekt_Sitedeployer]]:
        raise NotImplementedError("")

    @classmethod
    def ynsight_dependencies_all(cls) -> List[Type['Sitedeployer']]:
        return cls.ynsight_dependencies_common() + cls.ynsight_dependencies_self() + cls.workshop_projects()


    def Execute(self) -> None:
        pass
