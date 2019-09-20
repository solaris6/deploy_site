import os
import shutil
import subprocess
from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project
from sitedeployer.projects.core.Projekt import Projekt, logger
from sitedeployer.utils import log_environment


class Workshop(
    Projekt
):
    def __init__(self):
        Projekt.__init__(self)


    def Init(self) -> None:
        Projekt.Init(self)
        logger.info('Init Workshop...')
        logger.info(
'''PATHDIR_root_out_type_NAME_ver_output_os_ins_lib: '%PATHDIR_root_out_type_NAME_ver_output_os_ins_lib%'
'''
            .replace('', '')
        )
        logger.info('Init Workshop!')


    # names:
    def projekt(self) -> str:
        return 'workshop'


    # build:
    # as target:
    def install_as_target(self) -> None:
        logger.info('Install as target "%projekt%" projekt...'.replace('%projekt%', self.NAME()))
        self.clone_projekt()

        logger.info('Build and Install ("%projekt%")'.replace('%projekt%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projektrepository()
        )

        self._wsgipy_entry += \
'''# install_as_target:
sys.path = ['%PATHDIR_root_out_projekt%'] + sys.path'''\
            .replace('%PATHDIR_root_out_projekt%', str(self.PATHDIR_root_out_projekt()))

        logger.info('Build and Install ("%projekt%")!'.replace('%projekt%', self.NAME()))

        self._is_installed_as_target = True

        logger.info('Install as target "%projekt%" projekt!'.replace('%projekt%', self.NAME()))

    def report(self) -> str:
        return \
'''NAME: "%NAME%", is_installed_as_target: %is_installed_as_target%'''\
    .replace('%NAME%', self.NAME())\
    .replace('%is_installed_as_target%', str(1 if self.is_installed_as_target() else 0))
