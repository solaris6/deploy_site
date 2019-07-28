from pathlib import Path
from typing import Type, List

from targets.core.Projekttarget import Projekttarget
from targets.core.Target import Target, logger



class Workshoptarget(
    Target
):
    def projektorworkshop_Type(self) -> str:
        return 'workshop'

    def workshop_projects(self) -> List[Type[Projekttarget]]:
        raise NotImplementedError("")

    def ynsight_dependencies_all(self) -> List[Type['Target']]:
        return self.ynsight_dependencies_common() + self.ynsight_dependencies_self() + self.workshop_projects()
