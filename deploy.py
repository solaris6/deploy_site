import os
import shutil, subprocess
import sys
from copy import copy
from pathlib import Path
from typing import Type, List

from targets.core.Target import Target
from utils import log_environment

import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from targets.builtin.projekt.Ln_Projekttarget import Ln_Projekttarget
from targets.builtin.projekt.base_Projekttarget import base_Projekttarget
from targets.builtin.projekt.cgbase_Projekttarget import cgbase_Projekttarget
from targets.builtin.projekt.fw_Projekttarget import fw_Projekttarget
from targets.builtin.projekt.myrta_Projekttarget import myrta_Projekttarget
from targets.builtin.projekt.projekt_Projekttarget import projekt_Projekttarget
from targets.builtin.projekt.rs_Projekttarget import rs_Projekttarget
from targets.builtin.projekt.rsdata_Projekttarget import rsdata_Projekttarget
from targets.builtin.projekt.sc_Projekttarget import sc_Projekttarget
from targets.builtin.projekt.sola_Projekttarget import sola_Projekttarget
from targets.builtin.projekt.una_Projekttarget import una_Projekttarget
from targets.builtin.workshop.ynsight_Workshoptarget import ynsight_Workshoptarget

class Sitedeployer:
    def __init__(self,
        PATHFILE_deploypy:Path=None,
        target:Target=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy
        self._target = target

        self._PATH_old = None
        self._PYTHONPATH_old = None
        self._ynsight_projects_installed = []

    def target(self) -> Target:
        return self._target

    def pythonanywhere_username(self) -> str:
        return self.target().pythonanywhere_username()

    def URL_site(self) -> str:
        return self.pythonanywhere_username() + '.pythonanywhere.com'

    def PATHDIR_home_pythonanywhereusername_root(self) -> Path:
        return self._PATHFILE_deploypy.parent.parent.parent

    def PATHDIR_root(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root()

    def PATHDIR_home_pythonanywhereusername(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root().parent

    def PATHDIR_root_ins(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'ins'

    def PATHDIR_root_instemp(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'instemp'

    def PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy(self) -> Path:
        return self._PATHFILE_deploypy

    def PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage(self) -> Path:
        return self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy().parent

    def PATHDIR_home_pythonanywhereusername_root_sitedeployer(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage().parent

    def process_common(self) -> None:
        logger.info('Process common...')

        logger.info('Resolve common paths...')
        logger.info(
'''URL_site=%URL_site%

PATHDIR_home_pythonanywhereusername_root=%PATHDIR_home_pythonanywhereusername_root%
PATHDIR_home_pythonanywhereusername=%PATHDIR_home_pythonanywhereusername%

PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy=%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy%
PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage=%PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage%
PATHDIR_home_pythonanywhereusername_root_sitedeployer=%PATHDIR_home_pythonanywhereusername_root_sitedeployer%'''
            .replace('%URL_site%', str(self.URL_site()))
            \
            .replace('%PATHDIR_home_pythonanywhereusername_root%', str(self.PATHDIR_home_pythonanywhereusername_root()))
            .replace('%PATHDIR_home_pythonanywhereusername%', str(self.PATHDIR_home_pythonanywhereusername()))
            .replace('%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy%',
                     str(self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy()))
            .replace('%PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage%',
                     str(self.PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage()))
            .replace('%PATHDIR_home_pythonanywhereusername_root_sitedeployer%', str(self.PATHDIR_home_pythonanywhereusername_root_sitedeployer()))
        )
        logger.info('Resolve common paths!')

        logger.info('Make common dirs...')
        self.PATHDIR_root_ins().mkdir(parents=True)
        self.PATHDIR_root_instemp().mkdir(parents=True)
        logger.info('Make common dirs!')
        logger.info('Process common!')


    # temp ynsight dependencies:
    def process_temp_ynsight_dependencies(self) -> None:
        logger.info('Process temp ynsight dependencies...')
        for temp_ynsight_dependency in self.target().temp_ynsight_dependencies():
            logger.info('Process temp_ynsight_project: "%temp_ynsight_project%"...'.replace('%temp_ynsight_project%', temp_ynsight_dependency.NAME()))
            temp_ynsight_dependency(
                PATHFILE_deploypy=self._PATHFILE_deploypy
            ).clonebuildinstalltemp()
            logger.info('Process temp_ynsight_project: "%temp_ynsight_project%"!'.replace('%temp_ynsight_project%', temp_ynsight_dependency.NAME()))
        logger.info('Process temp ynsight dependencies!')


    # ynsight dependencies:
    def process_ynsight_dependencies(self) -> None:
        logger.info('Process ynsight dependencies...')
        for ynsight_dependency in self.target().ynsight_dependencies_all():
            ynsight_dependency=ynsight_dependency(
                PATHFILE_deploypy=self._PATHFILE_deploypy
            )
            logger.info('Clonebuildinstall ynsight project: "%ynsight_project%"...'.replace('%ynsight_project%', ynsight_dependency.NAME()))
            if not ynsight_dependency.NAME() in self._ynsight_projects_installed:
                self._ynsight_projects_installed.append(ynsight_dependency.NAME())
                ynsight_dependency.clonebuildinstall()
            logger.info('Clonebuildinstall ynsight project: "%ynsight_project%"!'.replace('%ynsight_project%', ynsight_dependency.NAME()))
        logger.info('Process ynsight dependencies!')


    # process project:
    def github_username(self) -> str:
        return 'ynsight'


    # wsgi.py:
    def PATHFILE_wsgipy(self) -> Path:
        return Path(
                '/var/www/%pythonanywhere_username%_pythonanywhere_com_wsgi.py'
                    .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            )

    def process_wsgipy(self) -> None:
        logger.info('Process wsgi.py...')
        logger.info(
'''wsgi.py paths:
PATHFILE_wsgipy=%PATHFILE_wsgipy%'''
            .replace('%PATHFILE_wsgipy%', str(self.PATHFILE_wsgipy()))
        )

        logger.info('Write wsgi.py file...')
        wsgipy_template = \
'''import sys, os
from pathlib import Path

PATHDIR_projektorworkshop = Path('/home/%pythonanywhere_username%/root/_%projektorworkshop%')
if not str(PATHDIR_projektorworkshop) in sys.path:
    sys.path = [str(PATHDIR_projektorworkshop)] + sys.path


# Append ynsight project`s packages to sys.paths:
%ynsight_projects_packages_syspaths_appends%

# Append ynsight project`s executables to PATH envvar:
%ynsight_projects_packages_PATH_appends%

from %projektorworkshop_projektorworkshopsitepubflaskpackage%.flask_app import app as application
'''

        ynsight_projects_packages_syspaths_appends = ''
        ynsight_projects_packages_PATH_appends = ''
        for i,ynsight_project_installed in enumerate(self._ynsight_projects_installed):
            ynsight_projects_packages_syspaths_appends += ('' if i==0 else '\n') +\
"os.environ['PATH'] += os.pathsep + '/home/%pythonanywhere_username%/root/ins/%dependency_NAME%/bin'"\
    .replace('%dependency_NAME%', ynsight_project_installed)

            ynsight_projects_packages_PATH_appends += ('' if i==0 else '\n') +\
"sys.path = ['/home/%pythonanywhere_username%/root/ins/%dependency_NAME%/lib'] + sys.path"\
    .replace('%dependency_NAME%', ynsight_project_installed)

        wsgipy_fc = wsgipy_template\
            .replace('%ynsight_projects_packages_syspaths_appends%', ynsight_projects_packages_syspaths_appends)\
            .replace('%ynsight_projects_packages_PATH_appends%', ynsight_projects_packages_PATH_appends)\
            .replace('%pythonanywhere_username%', self.target().pythonanywhere_username())\
            .replace('%projektorworkshop_projektorworkshopsitepubflaskpackage%', self.target().projektorworkshop_projektorworkshopsitepubflaskpackage())\
            .replace('%projektorworkshop%', self.target().projektorworkshop_Type())

        self.PATHFILE_wsgipy().write_text(
            wsgipy_fc
        )

        logger.info('WSGIPY_FILE_BEGIN' + wsgipy_fc + 'WSGIPY_FILE_END')
        logger.info('Write wsgi.py file!')
        logger.info('Process wsgi.py!')



    # update.py:
    def PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage() / 'update.py'

    def PATHFILE_home_pythonanywhereusername_updatepy(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername() / 'update.py'

    def process_updatepy(self) -> None:
        logger.info('Process update.py...')
        logger.info(
'''update.py paths:
PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy=%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy%
PATHFILE_home_pythonanywhereusername_updatepy=%PATHFILE_home_pythonanywhereusername_updatepy%'''
            .replace('%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy()))
            .replace('%PATHFILE_home_pythonanywhereusername_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_updatepy()))
        )

        logger.info('Write update.py file...')
        shutil.copyfile(
            self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy(),
            self.PATHFILE_home_pythonanywhereusername_updatepy()
        )
        logger.info('Write update.py file!')
        logger.info('Process update.py!')


    def Execute(self) -> None:
        log_environment(logger=logger)
        self.process_common()

        log_environment(logger=logger)
        self._PATH_old = copy(os.environ['PATH']) if 'PATH' in os.environ else ''
        self._PYTHONPATH_old = copy(os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else ''
        log_environment(logger=logger)

        self.process_temp_ynsight_dependencies()
        self.process_ynsight_dependencies()

        if not self.target().NAME() in self._ynsight_projects_installed:
            self._ynsight_projects_installed.append(self.target().NAME())
            self.target().clonebuildinstall()

        self.target().process_projektorworkshop()

        log_environment(logger=logger)
        os.environ['PATH'] = self._PATH_old
        os.environ['PYTHONPATH'] = self._PYTHONPATH_old
        log_environment(logger=logger)

        self.process_wsgipy()
        self.process_updatepy()



if __name__ == '__main__':
    logger.info('Deploy site...')
    PATHFILE_deploypy = Path(sys.argv[0])
    pythonanywhere_username = PATHFILE_deploypy.parent.parent.parent.parent.name

    Sitedeployer(
        PATHFILE_deploypy=PATHFILE_deploypy,
        target={
            'getbase': base_Projekttarget,
            'getprojekt': projekt_Projekttarget,
            'getmyrta': myrta_Projekttarget,
            'getuna': una_Projekttarget,
            'getrs': rs_Projekttarget,
            'getrsdata': rsdata_Projekttarget,
            'getsc': sc_Projekttarget,
            'getfw': fw_Projekttarget,
            'getsola': sola_Projekttarget,
            'getln': Ln_Projekttarget,
            'getcgbase': cgbase_Projekttarget,

            'ynsight': ynsight_Workshoptarget
        }[pythonanywhere_username]()
    ).Execute()

    logger.info('Deploy site!')
