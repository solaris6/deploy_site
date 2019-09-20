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
from sitedeployer.projects.builtin.project.Ln_Project import Ln_Project
from sitedeployer.projects.builtin.project.base_Project import base_Project
from sitedeployer.projects.builtin.project.basedata_Project import basedata_Project
from sitedeployer.projects.builtin.project.cgbase_Project import cgbase_Project
from sitedeployer.projects.builtin.project.fw_Project import fw_Project
from sitedeployer.projects.builtin.project.myrta_Project import myrta_Project
from sitedeployer.projects.builtin.project.projekt_Project import projekt_Project
from sitedeployer.projects.builtin.project.rs_Project import rs_Project
from sitedeployer.projects.builtin.project.rsdata_Project import rsdata_Project
from sitedeployer.projects.builtin.project.sc_Project import sc_Project
from sitedeployer.projects.builtin.project.skfb_Project import skfb_Project
from sitedeployer.projects.builtin.project.sola_Project import sola_Project
from sitedeployer.projects.builtin.project.una_Project import una_Project
from sitedeployer.projects.builtin.workshop.ynsight_Workshop import ynsight_Workshop


if __name__ == '__main__':
    logger.info('Deploy site...')
    PATHFILE_deploypy = Path(sys.argv[0])
    pythonanywhere_username = PATHFILE_deploypy.parent.parent.parent.name

    target_projekt = {
        'getbase': base_Project,
        'getbasedata': basedata_Project,
        'getprojekt': projekt_Project,
        'getmyrta': myrta_Project,
        'getuna': una_Project,
        'getrs': rs_Project,
        'getrsdata': rsdata_Project,
        'getsc': sc_Project,
        'skfb': skfb_Project,
        'getfw': fw_Project,
        'getsola': sola_Project,
        'getln': Ln_Project,
        'getcgbase': cgbase_Project,

        'ynsight': ynsight_Workshop
    }[pythonanywhere_username]()

    Sitedeployer(
        PATHFILE_deploypy=PATHFILE_deploypy,
        target_projekt=target_projekt
    ).Execute()

    logger.info('Deploy site!')
