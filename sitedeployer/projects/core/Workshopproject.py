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
            cwd=self.PATHDIR_root_projectrepository(),
            # shell=True
        )

        logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables...'.replace('%project%', self.NAME()))
        log_environment(logger=logger)
        os.environ['PATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/distrib/lnx/bin'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
        os.environ['PYTHONPATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/distrib/lnx/lib'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')
        log_environment(logger=logger)
        logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables!'.replace('%project%', self.NAME()))


        self._wsgipy_entry += \
'''sys.path = ['%PATHDIR_root%/_out/Release/%NAME%/_2019_2_0/_%projektorworkshop%'] + sys.path'''\
            .replace('%PATHDIR_root%', str(self.PATHDIR_root()))\
            .replace('%projektorworkshop%', self.projektorworkshop_Type())\
            .replace('%NAME%', self.NAME())


        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)
        self._is_installed_as_target = True
        logger.info('Install as target "%project%" project!'.replace('%project%', self.NAME()))


    def install_as_target_and_lib(self) -> None:
        logger.info('Install as target and lib "%project%" project...'.replace('%project%', self.NAME()))

        if not self.is_installed_as_target():
            self.clone_project()

            logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

            subprocess.run(
                ['projekt', 'task', 'build', 'default', 'execute'],
                cwd=self.PATHDIR_root_projectrepository(),
                # shell=True
            )

            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables...'.replace('%project%', self.NAME()))
            log_environment(logger=logger)
            os.environ['PATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/distrib/lnx/bin'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
            os.environ['PYTHONPATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/distrib/lnx/lib'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')
            log_environment(logger=logger)
            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables!'.replace('%project%', self.NAME()))


            self._wsgipy_entry += \
'''install_as_target_and_lib'''\
                .replace('%PATHDIR_root%', str(self.PATHDIR_root()))\
                .replace('%projektorworkshop%', self.projektorworkshop_Type())\
                .replace('%NAME%', self.NAME())


            logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

            log_environment(logger=logger)
            self._is_installed_as_target = True
            logger.info('Install as target and lib "%project%" project!'.replace('%project%', self.NAME()))
        else:
            logger.info('Install as target and lib "%project%" project already installed, skipped!'.replace('%project%', self.NAME()))


    def report(self) -> str:
        return \
'''NAME: "%NAME%", target: [%install_as_target_toggle%, %is_installed_as_target%]'''\
    .replace('%install_as_target_toggle%', str(self.install_as_target_toggle()))\
    .replace('%is_installed_as_target%', str(self.is_installed_as_target()))