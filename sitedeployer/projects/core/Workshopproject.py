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

    def projektorworkshop_Type(self) -> str:
        return 'workshop'

    def dependencies_workshop_Types(self) -> List[Type[Projektproject]]:
        raise NotImplementedError("")

    def dependencies_Types_all(self) -> List[Type['Project']]:
        from sitedeployer.utils import remove_duplicates
        return remove_duplicates(
            self.dependencies_lib_Types_all() +\
            self.dependencies_workshop_Types()
        )


    def is_installed(self) -> bool:
        return self.is_installed_as_target()


    def install_as_target(self) -> None:
        logger.info('Install as target "%project%" project...'.replace('%project%', self.NAME()))
        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self._wsgipy_entry += \
'''# install_as_target:
sys.path = ['%PATHDIR_root_out_proojektorworkshop%'] + sys.path'''\
            .replace('%PATHDIR_root_out_proojektorworkshop%', str(self.PATHDIR_root_out_proojektorworkshop()))


        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)
        self._is_installed_as_target = True
        logger.info('Install as target "%project%" project!'.replace('%project%', self.NAME()))


    def report(self) -> str:
        return \
'''NAME: "%NAME%", target: { t: %install_as_target_toggle%, i: %is_installed_as_target% }'''\
    .replace('%NAME%', self.NAME())\
    .replace('%install_as_target_toggle%', str(1 if self.install_as_target_toggle() else 0))\
    .replace('%is_installed_as_target%', str(1 if self.is_installed_as_target() else 0))