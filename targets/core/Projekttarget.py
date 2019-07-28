from pathlib import Path
from typing import List, Type

from targets.core.Target import Target, logger


class Projekttarget(
    Target
):
    def projektorworkshop_Type(self) -> str:
        return 'projekt'

    def ynsight_dependencies_all(self) -> List[Type['Target']]:
        return self.ynsight_dependencies_common() + self.ynsight_dependencies_self()
