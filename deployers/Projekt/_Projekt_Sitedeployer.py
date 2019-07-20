import os, shutil, subprocess, sys
from pathlib import Path
import logging
from typing import Type, List

from deployers._Sitedeployer.Sitedeployer import Sitedeployer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



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
