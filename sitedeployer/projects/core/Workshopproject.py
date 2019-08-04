import os
import shutil
import subprocess
from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Projektproject import Projektproject
from sitedeployer.projects.core.Project import Project, logger
from sitedeployer.utils import log_environment


class Workshopproject(
    Project
):
    def __init__(self):
        Project.__init__(self)


    def Init(self) -> None:
        Project.Init(self)
        logger.info('Init Workshopproject...')
        logger.info(
'''PATHDIR_root_out_type_NAME_ver_output_os_ins_lib: '%PATHDIR_root_out_type_NAME_ver_output_os_ins_lib%'
'''
            .replace('', '')
        )
        logger.info('Init Workshopproject!')


    # names:
    def projekt(self) -> str:
        return 'workshop'


    # dependencies:
    def dependencies_workshop_Types(self) -> List[Type[Projektproject]]:
        raise NotImplementedError("")

    def dependencies_Types_all(self) -> List[Type['Project']]:
        from sitedeployer.utils import remove_duplicates
        return remove_duplicates(
            self.dependencies_lib_Types_all() +\
            self.dependencies_workshop_Types()
        )


    # build:
    # as target:
    def install_as__target(self) -> None:
        logger.info('Install as target "%project%" project...'.replace('%project%', self.NAME()))
        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self._wsgipy_entry += \
'''# install_as__target:
sys.path = ['%PATHDIR_root_out_project%'] + sys.path'''\
            .replace('%PATHDIR_root_out_project%', str(self.PATHDIR_root_out_project()))

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        self._is_installed_as__target = True

        logger.info('Install as target "%project%" project!'.replace('%project%', self.NAME()))


    def install(self) -> None:
        self.install_as__target()


    def report(self) -> str:
        return \
'''NAME: "%NAME%", target: { t: %toggle_install_as__target%, i: %is_installed_as__target% }'''\
    .replace('%NAME%', self.NAME())\
    .replace('%toggle_install_as__target%', str(1 if self.toggle_install_as__target() else 0))\
    .replace('%is_installed_as__target%', str(1 if self.is_installed_as__target() else 0))
