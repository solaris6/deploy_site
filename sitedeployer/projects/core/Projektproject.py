import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Type

from sitedeployer.projects.core.Project import Project, logger
from sitedeployer.utils import log_environment


class Projektproject(
    Project
):
    def __init__(self):
        Project.__init__(self)

        self._install_as_temp_toggle = False
        self._is_installed_as_temp = False

        self._install_as_lib_toggle = False
        self._is_installed_as_lib = False

        self._install_as_workshopcard_toggle = False
        self._is_installed_as_workshopcard = False

    def projektorworkshop_Type(self) -> str:
        return 'projekt'

    def dependencies_Types_all(self) -> List[Type['Project']]:
        from sitedeployer.utils import remove_duplicates
        return remove_duplicates(self.dependencies_lib_Types_all())


    def is_installed(self) -> bool:
        return self.is_installed_as_lib() or self.is_installed_as_target() or self.is_installed_as_workshopcard()



    def set_install_as_temp_toggle(self,
        value:bool=None
    ) -> None:
        self._install_as_temp_toggle = value

    def install_as_temp_toggle(self) -> bool:
        return self._install_as_temp_toggle

    def is_installed_as_temp(self) -> bool:
        return self._is_installed_as_temp


    def install_as_temp(self) -> None:
        logger.info('Install as temp "%project%" project...'.replace('%project%', self.NAME()))

        if not self.is_installed_as_temp():
            self.clone_project()

            logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))
            PATHDIR_root_projectrepository_ins = self.PATHDIR_root_projectrepository() / 'src/ins'

            if PATHDIR_root_projectrepository_ins.is_dir() and not self.PATHDIR_root_instemp_project().is_dir():
                shutil.copytree(
                    PATHDIR_root_projectrepository_ins,
                    self.PATHDIR_root_instemp_project()
                )

            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables...'.replace('%project%', self.NAME()))
            log_environment(logger=logger)
            os.environ['PATH'] = str(self.PATHDIR_root_instemp_project() / 'bin') + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
            os.environ['PYTHONPATH'] = str(self.PATHDIR_root_instemp_project() / 'lib') + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')
            log_environment(logger=logger)
            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables!'.replace('%project%', self.NAME()))

            logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

            self._is_installed_as_temp = True
            logger.info('Install as temp "%project%" project!'.replace('%project%', self.NAME()))
        else:
            logger.info('Install as temp "%project%" project already installed, skipped!'.replace('%project%', self.NAME()))


    def uninstall_as_temp(self) -> None:
        logger.info('Uninstall as temp "%project%" project...'.replace('%project%', self.NAME()))

        if self.is_installed_as_temp():
            logger.info('Deleting "%project%" project %PATHDIR% directory...'
                .replace('%project%', self.NAME())
                .replace('%PATHDIR%', str(self.PATHDIR_root_instemp_project()))
            )
            if self.PATHDIR_root_instemp_project().is_dir():
                shutil.rmtree(self.PATHDIR_root_instemp_project())
                logger.info('Deleting "%project%" project %PATHDIR% directory!'
                    .replace('%project%', self.NAME())
                    .replace('%PATHDIR%', str(self.PATHDIR_root_instemp_project()))
                )
            else:
                logger.info('Deleting "%project%" project %PATHDIR% directory NOT exists, skipped...'
                    .replace('%project%', self.NAME())
                    .replace('%PATHDIR%', str(self.PATHDIR_root_instemp_project()))
                )

            logger.info('Deleting PATH and PYTHONPATH "%project%" project entries...'
                .replace('%project%', self.NAME())
                .replace('%PATHDIR%', str(self.PATHDIR_root_instemp_project()))
            )
            logger.info('Deleting PATH and PYTHONPATH "%project%" project entries!'
                .replace('%project%', self.NAME())
                .replace('%PATHDIR%', str(self.PATHDIR_root_instemp_project()))
            )

            logger.info('Uninstall as temp "%project%" project!'.replace('%project%', self.NAME()))
        else:
            logger.info('Uninstall as temp "%project%" project NOT installed as temp, skipped!'.replace('%project%', self.NAME()))



    def set_install_as_lib_toggle(self,
        value:bool=None
    ) -> None:
        self._install_as_lib_toggle = value

    def install_as_lib_toggle(self) -> bool:
        return self._install_as_lib_toggle

    def is_installed_as_lib(self) -> bool:
        return self._is_installed_as_lib

    def install_as_lib(self) -> None:
        logger.info('Install as lib "%project%" project...'.replace('%project%', self.NAME()))

        if not self.is_installed_as_target():
            self.clone_project()

            logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

            logger.info(str(self.sitedeployer()))
            logger.info(str(self.sitedeployer().PATHDIR_root()))
            logger.info(str(self.PATHDIR_root()))
            logger.info(str(self.PATHDIR_root_projectrepository()))
            logger.info(str(self.NAME()))

            subprocess.run(
                ['projekt', 'task', 'build', 'default', 'execute'],
                cwd=self.PATHDIR_root_projectrepository(),
                # shell=True
            )

            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables...'.replace('%project%', self.NAME()))
            log_environment(logger=logger)
            os.environ['PATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/ins/lnx/bin'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
            os.environ['PYTHONPATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/ins/lnx/lib'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')
            log_environment(logger=logger)
            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables!'.replace('%project%', self.NAME()))

            self.uninstall_as_temp()

            logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

            log_environment(logger=logger)
            self._is_installed_as_lib = True
            logger.info('Install as lib "%project%" project!'.replace('%project%', self.NAME()))
        else:
            logger.info('Install as lib "%project%" project already installed, skipped!'.replace('%project%', self.NAME()))





    def install_as_lib_and_workshopcard(self) -> None:
        logger.info('Install as lib and workshopcard "%project%" project...'.replace('%project%', self.NAME()))

        if not (self.is_installed_as_lib() or self.is_installed_as_workshopcard()):
            self.clone_project()

            logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

            subprocess.run(
                ['projekt', 'task', 'build', 'default', 'execute'],
                cwd=self.PATHDIR_root_projectrepository(),
                # shell=True
            )

            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables...'.replace('%project%', self.NAME()))
            log_environment(logger=logger)
            os.environ['PATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/ins/lnx/bin'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
            os.environ['PYTHONPATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/ins/lnx/lib'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')
            log_environment(logger=logger)
            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables!'.replace('%project%', self.NAME()))

            self.uninstall_as_temp()

            logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

            log_environment(logger=logger)

            self._is_installed_as_lib = True
            self._is_installed_as_workshopcard = True

            logger.info('Install as lib and workshopcard "%project%" project!'.replace('%project%', self.NAME()))
        else:
            logger.info('Install as lib and workshopcard "%project%" project already installed, skipped!'.replace('%project%', self.NAME()))





    def install_as_target(self) -> None:
        logger.info('Install as target "%project%" project...'.replace('%project%', self.NAME()))

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
            os.environ['PATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/ins/lnx/bin'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
            os.environ['PYTHONPATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/ins/lnx/lib'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')
            log_environment(logger=logger)
            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables!'.replace('%project%', self.NAME()))

            self.uninstall_as_temp()

            logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

            log_environment(logger=logger)
            self._is_installed_as_target = True
            logger.info('Install as target "%project%" project!'.replace('%project%', self.NAME()))
        else:
            logger.info('Install as target "%project%" project already installed, skipped!'.replace('%project%', self.NAME()))



    def set_install_as_workshopcard_toggle(self,
        value:bool=None
    ) -> None:
        self._install_as_workshopcard_toggle = value

    def install_as_workshopcard_toggle(self) -> bool:
        return self._install_as_workshopcard_toggle

    def is_installed_as_workshopcard(self) -> bool:
        return self._is_installed_as_workshopcard

    def install_as_workshopcard(self) -> None:
        logger.info('Install as workshopcard "%project%" project...'.replace('%project%', self.NAME()))

        if not self.is_installed_as_workshopcard():
            self.clone_project()

            logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

            subprocess.run(
                ['projekt', 'task', 'build', 'default', 'execute'],
                cwd=self.PATHDIR_root_projectrepository(),
                # shell=True
            )

            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables...'.replace('%project%', self.NAME()))
            log_environment(logger=logger)
            os.environ['PATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/ins/lnx/bin'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
            os.environ['PYTHONPATH'] = str(self.PATHDIR_root() / '_out/Release/%project%/_2019_2_0/ins/lnx/lib'.replace('%project%', self.NAME())) + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')
            log_environment(logger=logger)
            logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables!'.replace('%project%', self.NAME()))

            self.uninstall_as_temp()

            logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

            log_environment(logger=logger)
            self._is_installed_as_workshopcard = True
            logger.info('Install as workshopcard "%project%" project!'.replace('%project%', self.NAME()))
        else:
            logger.info('Install as workshopcard "%project%" project already installed, skipped!'.replace('%project%', self.NAME()))

    def report(self) -> str:
        return \
'''NAME: "%NAME%", temp: [%install_as_temp_toggle%, %is_installed_as_temp%], workshopcard: [%install_as_workshopcard_toggle%, %is_installed_as_workshopcard%], target: [%install_as_target_toggle%, %is_installed_as_target%], lib: [%install_as_lib_toggle%, %is_installed_as_lib%]'''\
    .replace('%install_as_temp_toggle%', str(self.install_as_temp_toggle()))\
    .replace('%is_installed_as_temp%', str(self.is_installed_as_temp()))\
    .replace('%install_as_workshopcard_toggle%', str(self.install_as_workshopcard_toggle()))\
    .replace('%is_installed_as_workshopcard%', str(self.is_installed_as_workshopcard()))\
    .replace('%install_as_target_toggle%', str(self.install_as_target_toggle()))\
    .replace('%is_installed_as_target%', str(self.is_installed_as_target()))\
    .replace('%install_as_lib_toggle%', str(self.install_as_lib_toggle()))\
    .replace('%is_installed_as_lib%', str(self.is_installed_as_lib()))