import logging
from sitedeployer.Gitproject._Gitproject.Gitproject import Gitproject

from sitedeployer.Gitproject.una_Gitproject import una_Gitproject
from sitedeployer.Gitproject.Ln_Gitproject import Ln_Gitproject
from sitedeployer.Gitproject.agent_Gitproject import agent_Gitproject
from sitedeployer.Gitproject.fw_Gitproject import fw_Gitproject
from sitedeployer.Gitproject.letters_Gitproject import letters_Gitproject
from sitedeployer.Gitproject.myrta_Gitproject import myrta_Gitproject
from sitedeployer.Gitproject.projekt_Gitproject import projekt_Gitproject
from sitedeployer.Gitproject.rs_Gitproject import rs_Gitproject
from sitedeployer.Gitproject.rsdata_Gitproject import rsdata_Gitproject
from sitedeployer.Gitproject.sc_Gitproject import sc_Gitproject
from sitedeployer.Gitproject.skfb_Gitproject import skfb_Gitproject
from sitedeployer.Gitproject.sola_Gitproject import sola_Gitproject
from sitedeployer.Gitproject.ynsbase_Gitproject import ynsbase_Gitproject
from sitedeployer.Gitproject.ynsight_Gitproject import ynsight_Gitproject

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from typing import List, Type

class Gitprojekts:

    @staticmethod
    def projekts_Types_all() -> List[Type[Gitproject]]:
        return [
            agent_Gitproject,
            fw_Gitproject,
            letters_Gitproject,
            Ln_Gitproject,
            myrta_Gitproject,
            projekt_Gitproject,
            rs_Gitproject,
            rsdata_Gitproject,
            sc_Gitproject,
            skfb_Gitproject,
            sola_Gitproject,
            una_Gitproject,
            ynsbase_Gitproject,

            ynsight_Gitproject
        ]


    def __init__(self):
        self._projekts_list = []
        for projekt_Type in self.projekts_Types_all():
            projekt = projekt_Type()
            projekt.attach_to_task(
                task=self
            )
            self._projekts_list.append(projekt)


    # pythonanywhere:
    def projekts_all(self) -> List[Gitproject]:
        return self._projekts_list