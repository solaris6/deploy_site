import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Type

from sitedeployer.projects.core.Project import Project, logger
from sitedeployer.utils import log_environment, lnx_mac_win


class Projektproject(
    Project
):
    def __init__(self):
        Project.__init__(self)

        self._toggle_install_as__temp = False
        self._is_installed_as__temp = False

        self._toggle_install_as__lib_deployer = False
        self._is_installed_as__lib_deployer = False

        self._toggle_install_as__lib_site = False
        self._is_installed_as__lib_site = False

        self._toggle_install_as__projektcard = False
        self._is_installed_as__projektcard = False


    def Init(self) -> None:
        Project.Init(self)
        logger.info('Init Projektproject...')
        logger.info(
'''# names:
projektcard_package: '%projektcard_package%'
PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin: '%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%'
PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib: '%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%'
'''
            .replace('%projektcard_package%', self.projektcard_package())
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin()))
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib()))
        )
        logger.info('Init Projektproject!')


    # names:
    def projektorworkshop(self) -> str:
        return 'projekt'

    def projektcard_package(self) -> str:
        return 'projektcard_%NAME%'\
            .replace('%NAME%', self.NAME())


    # PATHS:
    def PATHDIR_root_instemp_project_bin(self) -> Path:
        return self.PATHDIR_root_instemp_project() / 'bin'

    def PATHDIR_root_instemp_project_lib(self) -> Path:
        return self.PATHDIR_root_instemp_project() / 'lib'


    def PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin(self) -> Path:
        return self.PATHDIR_root() / '_out/Release/%NAME%/_2019_2_0/output/%os%/ins/bin'\
            .replace('%NAME%', self.NAME())\
            .replace('%os%', lnx_mac_win())

    def PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib(self) -> Path:
        return self.PATHDIR_root() / '_out/Release/%NAME%/_2019_2_0/output/%os%/ins/lib'\
            .replace('%NAME%', self.NAME())\
            .replace('%os%', lnx_mac_win())


    # dependencies:
    def dependencies_Types_all(self) -> List[Type['Project']]:
        from sitedeployer.utils import remove_duplicates
        return remove_duplicates(
            self.dependencies_lib_Types_all()
        )


    # build:
    def add_to_environment(self,
        as_temp:bool=False
    ) -> None:
        logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables...'.replace('%project%', self.NAME()))

        if as_temp:
            PATHDIR_bin = self.PATHDIR_root_instemp_project_bin()
            PATHDIR_lib = self.PATHDIR_root_instemp_project_lib()
        else:
            PATHDIR_bin = self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin()
            PATHDIR_lib = self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib()

        log_environment(logger=logger)
        os.environ['PATH'] = str(PATHDIR_bin) + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
        os.environ['PYTHONPATH'] = str(PATHDIR_lib) + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')
        log_environment(logger=logger)

        logger.info('Adding "%project%" project to PATH and PYTHONPATH environment variables!'.replace('%project%', self.NAME()))


    # as temp:
    def set_toggle_install_as__temp(self,
        value:bool=None
    ) -> None:
        self._toggle_install_as__temp = value

    def toggle_install_as__temp(self) -> bool:
        return self._toggle_install_as__temp

    def is_installed_as__temp(self) -> bool:
        return self._is_installed_as__temp


    def install_as__temp(self) -> None:
        logger.info('Install as temp "%project%" project...'.replace('%project%', self.NAME()))

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))
        PATHDIR_root_projectrepository_ins = self.PATHDIR_root_projectrepository() / 'src/ins'

        if PATHDIR_root_projectrepository_ins.is_dir() and not self.PATHDIR_root_instemp_project().is_dir():
            shutil.copytree(
                PATHDIR_root_projectrepository_ins,
                self.PATHDIR_root_instemp_project()
            )

        self.add_to_environment(
            as_temp=True
        )

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        self._is_installed_as__temp = True

        logger.info('Install as temp "%project%" project!'.replace('%project%', self.NAME()))


    def uninstall_as__temp(self) -> None:
        logger.info('Uninstall as temp "%project%" project...'.replace('%project%', self.NAME()))

        if self.is_installed_as__temp():
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


    # as lib deployer:
    def set_toggle_install_as__lib_deployer(self,
        value:bool=None
    ) -> None:
        self._toggle_install_as__lib_deployer = value

    def toggle_install_as__lib_deployer(self) -> bool:
        return self._toggle_install_as__lib_deployer

    def is_installed_as__lib_deployer(self) -> bool:
        return self._is_installed_as__lib_deployer

    def install_as__lib_deployer(self) -> None:
        logger.info('Install as lib deployer "%project%" project...'.replace('%project%', self.NAME()))

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self.add_to_environment()

        self._wsgipy_entry += \
"""# install_as_lib:
sys.path = ['%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%'] + sys.path
os.environ['PATH'] += os.pathsep + '%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%'"""\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib()))\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin()))


        self.uninstall_as__temp()

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)

        self._is_installed_as__lib_deployer = True

        logger.info('Install as lib deployer "%project%" project!'.replace('%project%', self.NAME()))

    # as lib site:
    def set_toggle_install_as__lib_site(self,
        value:bool=None
    ) -> None:
        self._toggle_install_as__lib_site = value

    def toggle_install_as__lib_site(self) -> bool:
        return self._toggle_install_as__lib_site

    def is_installed_as__lib_site(self) -> bool:
        return self._is_installed_as__lib_site

    def install_as__lib_site(self) -> None:
        logger.info('Install as as lib site "%project%" project...'.replace('%project%', self.NAME()))

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self.add_to_environment()

        self._wsgipy_entry += \
"""# install_as_lib:
sys.path = ['%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%'] + sys.path
os.environ['PATH'] += os.pathsep + '%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%'"""\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib()))\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin()))


        self.uninstall_as__temp()

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)

        self._is_installed_as__lib_site = True

        logger.info('Install as lib site "%project%" project!'.replace('%project%', self.NAME()))

    # as lib deployer, lib site:
    def install_as__lib_deployer__lib_site(self) -> None:
        logger.info('Install as lib deployer, lib site "%project%" project...'.replace('%project%', self.NAME()))

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self.add_to_environment()

        self._wsgipy_entry += \
"""# install_as_lib:
sys.path = ['%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%'] + sys.path
os.environ['PATH'] += os.pathsep + '%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%'"""\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib()))\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin()))


        self.uninstall_as__temp()

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)

        self._is_installed_as__lib_deployer = True
        self._is_installed_as__lib_site = True

        logger.info('Install as lib deployer, lib site "%project%" project!'.replace('%project%', self.NAME()))


    # as lib deployer, projektcard:
    def install_as__lib_deployer__projektcard(self) -> None:
        logger.info('Install as lib deployer, projektcard "%project%" project...'.replace('%project%', self.NAME()))

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self.add_to_environment()

        self._wsgipy_entry += \
"""# install_as_lib_and_projektcard:
sys.path = ['%PATHDIR_root_out_proojektorworkshop%'] + sys.path
sys.path = ['%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%'] + sys.path
os.environ['PATH'] += os.pathsep + '%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%'"""\
            .replace('%PATHDIR_root_out_proojektorworkshop%', str(self.PATHDIR_root_out_proojektorworkshop()))\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib()))\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin()))


        self.uninstall_as__temp()

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)

        self._is_installed_as__lib_deployer = True
        self._is_installed_as__projektcard = True

        logger.info('Install as lib deployer, projektcard "%project%" project!'.replace('%project%', self.NAME()))


    # as lib site, projektcard:
    def install_as__lib_site__projektcard(self) -> None:
        logger.info('Install as lib site, projektcard "%project%" project...'.replace('%project%', self.NAME()))

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self.add_to_environment()

        self._wsgipy_entry += \
"""# install_as_lib_and_projektcard:
sys.path = ['%PATHDIR_root_out_proojektorworkshop%'] + sys.path
sys.path = ['%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%'] + sys.path
os.environ['PATH'] += os.pathsep + '%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%'"""\
            .replace('%PATHDIR_root_out_proojektorworkshop%', str(self.PATHDIR_root_out_proojektorworkshop()))\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib()))\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin()))


        self.uninstall_as__temp()

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)

        self._is_installed_as__lib_site = True
        self._is_installed_as__projektcard = True

        logger.info('Install as lib site, projektcard "%project%" project!'.replace('%project%', self.NAME()))


    # as_lib_deployer, lib_site,_projektcard:
    def install_as__lib_deployer__lib_site__projektcard(self) -> None:
        logger.info('Install as_lib_deployer, lib_site,_projektcard "%project%" project...'.replace('%project%', self.NAME()))

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self.add_to_environment()

        self._wsgipy_entry += \
"""# install_as_lib_and_projektcard:
sys.path = ['%PATHDIR_root_out_proojektorworkshop%'] + sys.path
sys.path = ['%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%'] + sys.path
os.environ['PATH'] += os.pathsep + '%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%'"""\
            .replace('%PATHDIR_root_out_proojektorworkshop%', str(self.PATHDIR_root_out_proojektorworkshop()))\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_lib()))\
            .replace('%PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin%', str(self.PATHDIR_root_out_type_NAME_ver_distrib_os_ins_bin()))


        self.uninstall_as__temp()

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)

        self._is_installed_as__lib_deployer = True
        self._is_installed_as__lib_site = True
        self._is_installed_as__projektcard = True

        logger.info('Install as_lib_deployer, lib_site,_projektcard "%project%" project!'.replace('%project%', self.NAME()))


    # as projektcard:
    def set_toggle_install_as__projektcard(self,
        value:bool=None
    ) -> None:
        self._toggle_install_as__projektcard = value

    def toggle_install_as__projektcard(self) -> bool:
        return self._toggle_install_as__projektcard

    def is_installed_as__projektcard(self) -> bool:
        return self._is_installed_as__projektcard

    def install_as__projektcard(self) -> None:
        logger.info('Install as projektcard "%project%" project...'.replace('%project%', self.NAME()))

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self._wsgipy_entry += \
'''# install_as__projektcard
sys.path = ['%PATHDIR_root_out_proojektorworkshop%'] + sys.path'''\
            .replace('%PATHDIR_root_out_proojektorworkshop%', str(self.PATHDIR_root_out_proojektorworkshop()))

        self.uninstall_as__temp()

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)

        self._is_installed_as__projektcard = True

        logger.info('Install as projektcard "%project%" project!'.replace('%project%', self.NAME()))


    # as target:
    def install_as__target(self) -> None:
        logger.info('Install as target "%project%" project...'.replace('%project%', self.NAME()))

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository()
        )

        self.add_to_environment()

        self._wsgipy_entry += \
'''# install_as__target:
sys.path = ['%PATHDIR_root_out_proojektorworkshop%'] + sys.path'''\
            .replace('%PATHDIR_root_out_proojektorworkshop%', str(self.PATHDIR_root_out_proojektorworkshop()))

        self.uninstall_as__temp()

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)

        self._is_installed_as__target = True

        logger.info('Install as target "%project%" project!'.replace('%project%', self.NAME()))


    def install_as_dependency(self) -> None:
        if self.toggle_install_as__lib_deployer() and self.toggle_install_as__lib_site() and self.toggle_install_as__projektcard():
            self.install_as__lib_deployer__lib_site__projektcard()

        elif self.toggle_install_as__lib_deployer() and self.toggle_install_as__lib_site():
            self.install_as__lib_deployer__lib_site()

        elif self.toggle_install_as__lib_deployer() and self.toggle_install_as__projektcard():
            self.install_as__lib_deployer__projektcard()

        elif self.toggle_install_as__lib_site() and self.toggle_install_as__projektcard():
            self.install_as__lib_site__projektcard()

        elif self.toggle_install_as__lib_site():
            self.install_as__lib_site()

        elif self.toggle_install_as__lib_deployer():
            self.install_as__lib_deployer()

        elif self.toggle_install_as__projektcard():
            self.install_as__projektcard()


    def report(self) -> str:
        return \
'''NAME: "%NAME%", temp: { t: %toggle_install_as__temp%, i: %is_installed_as__temp% }, projektcard: { t: %toggle_install_as__projektcard%, i: %is_installed_as__projektcard% }, target: { t: %install_as__target_toggle%, i: %is_installed_as__target% }, lib_deployer: { t: %toggle_install_as__lib_deployer%, i: %is_installed_as__lib_deployer% }, lib_site: { t: %toggle_install_as__lib_site%, i: %is_installed_as__lib_site% }'''\
    .replace('%NAME%', self.NAME())\
    .replace('%toggle_install_as__temp%',         str(1 if self.toggle_install_as__temp() else 0))\
    .replace('%is_installed_as__temp%',           str(1 if self.is_installed_as__temp() else 0))\
    \
    .replace('%toggle_install_as__projektcard%',  str(1 if self.toggle_install_as__projektcard() else 0))\
    .replace('%is_installed_as__projektcard%',    str(1 if self.is_installed_as__projektcard() else 0))\
    \
    .replace('%install_as__target_toggle%',       str(1 if self.install_as__target_toggle() else 0))\
    .replace('%is_installed_as__target%',         str(1 if self.is_installed_as__target() else 0))\
    \
    .replace('%toggle_install_as__lib_deployer%', str(1 if self.toggle_install_as__lib_deployer() else 0))\
    .replace('%is_installed_as__lib_deployer%',   str(1 if self.is_installed_as__lib_deployer() else 0))\
    \
    .replace('%toggle_install_as__lib_site%',     str(1 if self.toggle_install_as__lib_site() else 0))\
    .replace('%is_installed_as__lib_site%',       str(1 if self.is_installed_as__lib_site() else 0))
