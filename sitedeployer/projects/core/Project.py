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

        self._toggle_install_as__dependency = False
        self._is_installed_as__dependency = False


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
    def set_toggle_install_as__dependency(self,
        value:bool=None
    ) -> None:
        self._toggle_install_as__dependency = value

    def toggle_install_as__dependency(self) -> bool:
        return self._toggle_install_as__dependency

    def is_installed_as__dependency(self) -> bool:
        return self._is_installed_as__dependency

    def install_as__dependency(self) -> None:
        logger.info('Install as as lib "%projekt%" projekt...'.replace('%projekt%', self.NAME()))

        self.clone_projekt()

        logger.info('Build and Install ("%projekt%")'.replace('%projekt%', self.NAME()))

        subprocess.run(
            ['python3.6', 'setup.py', 'install'],
            cwd=self.PATHDIR_root_projektrepository()
        )

        logger.info('Build and Install ("%projekt%")!'.replace('%projekt%', self.NAME()))

        self._is_installed_as__dependency = True

        logger.info('Install as lib "%projekt%" projekt!'.replace('%projekt%', self.NAME()))


    # as target:
    def install_as__target(self) -> None:
        logger.info('Install as target "%projekt%" projekt...'.replace('%projekt%', self.NAME()))

        self.clone_projekt()

        logger.info('Build and Install ("%projekt%")'.replace('%projekt%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projektrepository()
        )

        self._wsgipy_entry += \
'''# install_as__target():
sys.path = ['%PATHDIR_root_out_projekt%'] + sys.path'''\
            .replace('%PATHDIR_root_out_projekt%', str(self.PATHDIR_root_out_projekt()))

        logger.info('Build and Install ("%projekt%")!'.replace('%projekt%', self.NAME()))

        self._is_installed_as__target = True

        logger.info('Install as target "%projekt%" projekt!'.replace('%projekt%', self.NAME()))


    def install(self) -> None:
        if   self.toggle_install_as__target():
            self.install_as__target()

        elif self.toggle_install_as__dependency():
            self.install_as__dependency()


    def report(self) -> str:
        return \
'''NAME: "%NAME%", target: { t: %toggle_install_as__target%, i: %is_installed_as__target% }, dependency: { t: %toggle_install_as__dependency%, i: %is_installed_as__dependency% }'''\
    .replace('%NAME%', self.NAME())\
    \
    .replace('%toggle_install_as__target%', str(1 if self.toggle_install_as__target() else 0))\
    .replace('%is_installed_as__target%',   str(1 if self.is_installed_as__target() else 0))\
    \
    .replace('%toggle_install_as__dependency%',    str(1 if self.toggle_install_as__dependency() else 0))\
    .replace('%is_installed_as__dependency%',      str(1 if self.is_installed_as__dependency() else 0))
