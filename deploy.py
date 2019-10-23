import os
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

from sitedeployer.Projekt.Project.Ln_Project import Ln_Project
from sitedeployer.Projekt.Project.ynsbase_Project import ynsbase_Project
from sitedeployer.Projekt.Project.ynsbasedata_Project import ynsbasedata_Project
from sitedeployer.Projekt.Project.cgbase_Project import cgbase_Project
from sitedeployer.Projekt.Project.fw_Project import fw_Project
from sitedeployer.Projekt.Project.myrta_Project import myrta_Project
from sitedeployer.Projekt.Project.projekt_Project import projekt_Project
from sitedeployer.Projekt.Project.rs_Project import rs_Project
from sitedeployer.Projekt.Project.rsdata_Project import rsdata_Project
from sitedeployer.Projekt.Project.sc_Project import sc_Project
from sitedeployer.Projekt.Project.skfb_Project import skfb_Project
from sitedeployer.Projekt.Project.sola_Project import sola_Project
from sitedeployer.Projekt.Project.una_Project import una_Project
from sitedeployer.Projekt.Workshop.ynsight_Workshop import ynsight_Workshop

from sitedeployer.Sitedeployer import Sitedeployer


if __name__ == '__main__':
    logger.info('Deploy site...')
    PATHFILE_deploypy = Path(sys.argv[0])
    PATHDIR_deploypy = PATHFILE_deploypy.parent
    pythonanywhere_username = PATHFILE_deploypy.parent.parent.parent.name

    target_project = {
        'getbase': ynsbase_Project,
        'getbasedata': ynsbasedata_Project,
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

    PATHFILE_YNSIGHT_GITHUB_TOKEN_txt = PATHDIR_deploypy.parent.parent / 'YNSIGHT_GITHUB_TOKEN.txt'
    if PATHFILE_YNSIGHT_GITHUB_TOKEN_txt.is_file():
        YNSIGHT_GITHUB_TOKEN = PATHFILE_YNSIGHT_GITHUB_TOKEN_txt.read_text()
        os.environ['YNSIGHT_GITHUB_TOKEN'] = YNSIGHT_GITHUB_TOKEN

    Sitedeployer(
        PATHFILE_deploypy=PATHFILE_deploypy,
        target_project=target_project
    ).Execute()

    logger.info('Deploy site!')
