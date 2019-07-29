import sys
from pathlib import Path
sys.path.append(str(Path(sys.argv[0]).parent))

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from sitedeployer.Sitedeployer import Sitedeployer
from sitedeployer.projects.builtin.projekt.Ln_Projektproject import Ln_Projektproject
from sitedeployer.projects.builtin.projekt.base_Projektproject import base_Projektproject
from sitedeployer.projects.builtin.projekt.cgbase_Projektproject import cgbase_Projektproject
from sitedeployer.projects.builtin.projekt.fw_Projektproject import fw_Projektproject
from sitedeployer.projects.builtin.projekt.myrta_Projektproject import myrta_Projektproject
from sitedeployer.projects.builtin.projekt.projekt_Projektproject import projekt_Projektproject
from sitedeployer.projects.builtin.projekt.rs_Projektproject import rs_Projektproject
from sitedeployer.projects.builtin.projekt.rsdata_Projektproject import rsdata_Projektproject
from sitedeployer.projects.builtin.projekt.sc_Projektproject import sc_Projektproject
from sitedeployer.projects.builtin.projekt.sola_Projektproject import sola_Projektproject
from sitedeployer.projects.builtin.projekt.una_Projektproject import una_Projektproject
from sitedeployer.projects.builtin.workshop.ynsight_Workshopproject import ynsight_Workshopproject


if __name__ == '__main__':
    logger.info('Deploy site...')
    PATHFILE_deploypy = Path(sys.argv[0])
    pythonanywhere_username = PATHFILE_deploypy.parent.parent.parent.name

    target_project = {
        'getbase': base_Projektproject,
        'getprojekt': projekt_Projektproject,
        'getmyrta': myrta_Projektproject,
        'getuna': una_Projektproject,
        'getrs': rs_Projektproject,
        'getrsdata': rsdata_Projektproject,
        'getsc': sc_Projektproject,
        'getfw': fw_Projektproject,
        'getsola': sola_Projektproject,
        'getln': Ln_Projektproject,
        'getcgbase': cgbase_Projektproject,

        'ynsight': ynsight_Workshopproject
    }[pythonanywhere_username]()

    target_project.set_install_as_target_toggle(value=True)

    Sitedeployer(
        PATHFILE_deploypy=PATHFILE_deploypy,
        target_project=target_project
    ).Execute()

    logger.info('Deploy site!')
