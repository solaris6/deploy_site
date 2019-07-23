from pathlib import Path
from typing import List, Type

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

    @classmethod
    def ynsight_dependencies_all(cls) -> List[Type['Sitedeployer']]:
        return cls.ynsight_dependencies_common() + cls.ynsight_dependencies_self()

    def Execute(self) -> None:
        pass