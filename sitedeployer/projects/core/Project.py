import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Type

from sitedeployer.projects.core.Projekt import Projekt, logger
from sitedeployer.utils import log_environment, lnx_mac_win


class Project(
    Projekt
):
    def __init__(self):
        Projekt.__init__(self)

        self._is_installed_as_package = False


    def Init(self) -> None:
        Projekt.Init(self)
        logger.info('Init Project...')
        logger.info(
'''# names:
PATHDIR_root_out_type_NAME_ver_output_os_ins_bin: '%PATHDIR_root_out_type_NAME_ver_output_os_ins_bin%'
PATHDIR_root_out_type_NAME_ver_output_os_ins_lib: '%PATHDIR_root_out_type_NAME_ver_output_os_ins_lib%'
'''
            .replace('%PATHDIR_root_out_type_NAME_ver_output_os_ins_bin%', str(self.PATHDIR_root_out_type_NAME_ver_output_os_ins_bin()))
            .replace('%PATHDIR_root_out_type_NAME_ver_output_os_ins_lib%', str(self.PATHDIR_root_out_type_NAME_ver_output_os_ins_lib()))
        )
        logger.info('Init Project!')


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



    # as lib site:
    def is_installed_as_package(self) -> bool:
        return self._is_installed_as_package

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
        logger.info('Build and Install ("%projekt%")'.replace('%projekt%', self.NAME()))

        subprocess.run(
            ['python3.6', 'setup.py', 'install'],
            cwd=self.PATHDIR_root_projektrepository()
        )

        logger.info('Build and Install ("%projekt%")!'.replace('%projekt%', self.NAME()))

        self._is_installed_as_package = True

        logger.info('Install as package "%projekt%" projekt!'.replace('%projekt%', self.NAME()))


    def report(self) -> str:
        return \
'''NAME: "%NAME%", is_installed_as_target: %is_installed_as_target%, is_installed_as_package: %is_installed_as_package%'''\
    .replace('%NAME%', self.NAME())\
    \
    .replace('%is_installed_as_target%', str(1 if self.is_installed_as_target() else 0))\
    .replace('%is_installed_as_package%', str(1 if self.is_installed_as_package() else 0))
