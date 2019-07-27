import sys
from pathlib import Path

import logging

from deployers.builtin.projekt.Ln_ProjektSitedeployer import Ln_ProjektSitedeployer
from deployers.builtin.projekt.base_ProjektSitedeployer import base_ProjektSitedeployer
from deployers.builtin.projekt.cgbase_ProjektSitedeployer import cgbase_ProjektSitedeployer
from deployers.builtin.projekt.fw_ProjektSitedeployer import fw_ProjektSitedeployer
from deployers.builtin.projekt.myrta_ProjektSitedeployer import myrta_ProjektSitedeployer
from deployers.builtin.projekt.projekt_ProjektSitedeployer import projekt_ProjektSitedeployer
from deployers.builtin.projekt.rs_ProjektSitedeployer import rs_ProjektSitedeployer
from deployers.builtin.projekt.rsdata_ProjektSitedeployer import rsdata_ProjektSitedeployer
from deployers.builtin.projekt.sc_ProjektSitedeployer import sc_ProjektSitedeployer
from deployers.builtin.projekt.sola_ProjektSitedeployer import sola_ProjektSitedeployer
from deployers.builtin.projekt.una_ProjektSitedeployer import una_ProjektSitedeployer
from deployers.builtin.workshop.ynsight_WorkshopSitedeployer import ynsight_WorkshopSitedeployer

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deploy] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

if __name__ == '__main__':
    logger.info('Deploy site...')
    PATHFILE_deploypy = Path(sys.argv[0])
    pythonanywhere_username = PATHFILE_deploypy.parent.parent.parent.parent.name
    {
        'getbase': base_ProjektSitedeployer,
        'getprojekt': projekt_ProjektSitedeployer,
        'getmyrta': myrta_ProjektSitedeployer,
        'getuna': una_ProjektSitedeployer,
        'getrs': rs_ProjektSitedeployer,
        'getrsdata': rsdata_ProjektSitedeployer,
        'getsc': sc_ProjektSitedeployer,
        'getfw': fw_ProjektSitedeployer,
        'getsola': sola_ProjektSitedeployer,
        'getln': Ln_ProjektSitedeployer,
        'getcgbase': cgbase_ProjektSitedeployer,

        'ynsight': ynsight_WorkshopSitedeployer
    }[pythonanywhere_username](
        PATHFILE_deploypy=PATHFILE_deploypy
    )._Execute()

    logger.info('Deploy site!')
