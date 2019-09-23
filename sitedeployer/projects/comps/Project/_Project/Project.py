import os
import shutil
import subprocess
from pathlib import Path

from sitedeployer.projects.comps._Projekt.Projekt import Projekt
from sitedeployer.utils import lnx_mac_win

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[sitedeployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class Project(
    Projekt
):
    def __init__(self):
        Projekt.__init__(self)


    # names:
    def projekt(self) -> str:
        return 'project'


    # PATHS:
    def PATHDIR_root_out_type_NAME_ver_output_os_ins_bin(self) -> Path:
        return self.PATHDIR_root() / '_out/Release/%NAME%/_2019_2_0/output/%os%/ins/bin'\
            .replace('%NAME%', self.NAME())\
            .replace('%os%', lnx_mac_win())

    def PATHDIR_root_out_type_NAME_ver_output_os_ins_lib(self) -> Path:
        return self.PATHDIR_root() / '_out/Release/%NAME%/_2019_2_0/output/%os%/ins/lib'\
            .replace('%NAME%', self.NAME())\
            .replace('%os%', lnx_mac_win())



    def install_as_package(self) -> None:

        logger.info('Uninstall "%projekt%" first...'.replace('%projekt%', self.NAME()))

        PATHDIR_sitepackages = Path(
            '/home/%pythonanywhere_username%/.virtualenvs/python36venv/lib/python3.6/site-packages'\
                .replace('%pythonanywhere_username%', self.sitedeployer().pythonanywhere_username())
        )

        prev_installation_exists = False
        if PATHDIR_sitepackages.is_dir():
            for item in os.listdir(PATHDIR_sitepackages):
                PATHDIR_egg = PATHDIR_sitepackages / item
                if item.startswith(self.NAME()) and item.endswith('-py3.6.egg') and PATHDIR_egg.is_dir():
                    logger.info('Previous installation exists, deleting("' + str(PATHDIR_egg) + '")...')
                    shutil.rmtree(PATHDIR_egg)
                    prev_installation_exists = True

        if not prev_installation_exists:
            logger.info('Previous installation NOT exists, skipping')
        logger.info('Uninstall "%projekt%" first!'.replace('%projekt%', self.NAME()))


        logger.info('Install as as package "%projekt%" projekt...'.replace('%projekt%', self.NAME()))
        self.clone_projekt()

        subprocess.run(
            ['python3.6', 'setup.py', 'install'],
            cwd=self.PATHDIR_root_projektrepository()
        )

        logger.info('Install as package "%projekt%" projekt!'.replace('%projekt%', self.NAME()))
