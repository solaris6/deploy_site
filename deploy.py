import os
import shutil, subprocess
import sys
from copy import copy
from pathlib import Path
from typing import Type, List

from projects.core.Project import Project
from projects.core.Workshopproject import Workshopproject
from utils import log_environment

import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from projects.builtin.projekt.Ln_Projektproject import Ln_Projektproject
from projects.builtin.projekt.base_Projektproject import base_Projektproject
from projects.builtin.projekt.cgbase_Projektproject import cgbase_Projektproject
from projects.builtin.projekt.fw_Projektproject import fw_Projektproject
from projects.builtin.projekt.myrta_Projektproject import myrta_Projektproject
from projects.builtin.projekt.projekt_Projektproject import projekt_Projektproject
from projects.builtin.projekt.rs_Projektproject import rs_Projektproject
from projects.builtin.projekt.rsdata_Projektproject import rsdata_Projektproject
from projects.builtin.projekt.sc_Projektproject import sc_Projektproject
from projects.builtin.projekt.sola_Projektproject import sola_Projektproject
from projects.builtin.projekt.una_Projektproject import una_Projektproject
from projects.builtin.workshop.ynsight_Workshopproject import ynsight_Workshopproject


class Sitedeployer:
    def __init__(self,
        PATHFILE_deploypy:Path=None,
        target_project:Project=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy
        self._target_project = target_project

        self._PATH_old = None
        self._PYTHONPATH_old = None

    def target_project(self) -> Project:
        return self._target_project

    def pythonanywhere_username(self) -> str:
        return self.target_project().pythonanywhere_username()

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


# Append project`s packages to sys.paths:
%projects_packages_syspaths_appends%

# Append project`s executables to PATH envvar:
%projects_packages_PATH_appends%

from %projektorworkshop_projektorworkshopsitepubflaskpackage%.flask_app import app as application
'''

        projects_packages_syspaths_appends = ''
        projects_packages_PATH_appends = ''
        for i,project_installed in enumerate(self._projects_installed):
            projects_packages_syspaths_appends += ('' if i==0 else '\n') +\
"os.environ['PATH'] += os.pathsep + '/home/%pythonanywhere_username%/root/ins/%dependency_NAME%/bin'"\
    .replace('%dependency_NAME%', project_installed)

            projects_packages_PATH_appends += ('' if i==0 else '\n') +\
"sys.path = ['/home/%pythonanywhere_username%/root/ins/%dependency_NAME%/lib'] + sys.path"\
    .replace('%dependency_NAME%', project_installed)

        wsgipy_fc = wsgipy_template\
            .replace('%projects_packages_syspaths_appends%', projects_packages_syspaths_appends)\
            .replace('%projects_packages_PATH_appends%', projects_packages_PATH_appends)\
            .replace('%pythonanywhere_username%', self.target_project().pythonanywhere_username())\
            .replace('%projektorworkshop_projektorworkshopsitepubflaskpackage%', self.target().projektorworkshop_projektorworkshopsitepubflaskpackage())\
            .replace('%projektorworkshop%', self.target_project().projektorworkshop_Type())

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
        projects_all = []

        for project_Type in self.target_project().dependencies_Types_all():
            if not project_Type is type(self.target_project()):
                projects_all.append(
                    project_Type()
                )

        projects_all += self.target_project()

        for project in projects_all:
            project.attach_to_sitedeployer(
                sitedeployer=self
            )

        for project in projects_all:
            if type(project) in self.target_project().dependencies_lib_temp_Types():
                project.set_install_as_temp_toggle(
                    value=True
                )

            if type(project) in self.target_project().dependencies_lib_Types_all():
                project.set_install_as_lib_toggle(
                    value=True
                )

            if isinstance(self.target_project(), Workshopproject) and\
                type(project) in self.target_project().dependencies_workshop_Types():
                project.set_install_as_workshopcard_toggle(
                    value=True
                )

        log_environment(logger=logger)
        self.process_common()

        log_environment(logger=logger)
        self._PATH_old = copy(os.environ['PATH']) if 'PATH' in os.environ else ''
        self._PYTHONPATH_old = copy(os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else ''
        log_environment(logger=logger)

        logger.info('Process temp dependencies...')
        for project in projects_all:
            if project.install_as_temp_toggle():
                project.install_as_temp()
        logger.info('Process temp dependencies!')


        logger.info('Process lib/workshopcard dependencies...')
        for projekt in projects_all:
            if projekt.install_as_lib_toggle() and projekt.install_as_workshopcard_toggle():
                project.install_as_lib_and_workshopcard()

            elif projekt.install_as_lib_toggle():
                project.install_as_lib()

            elif projekt.install_as_workshopcard_toggle():
                project.install_as_workshopcard()
        logger.info('Process lib/workshopcard dependencies!')

        self.target_project().install_as_target()

        self.target_project().process_projektorworkshop()

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

    target_project = {
        'getbase': base_Projektproject,
        'getprojekt': projekt_Projektproject,
        'getmyrta': myrta_Projektproject,
        'getuna': una_Projektproject,
        'getrs': rs_Projektproject,
        'getrsdata': rsdata_Projektproject,
        'getsc': sc_Projektproject,
        'getfw': fw_Projektproject,
        'getsola': sola_Projektproject,
        'getln': Ln_Projektproject,
        'getcgbase': cgbase_Projektproject,

        'ynsight': ynsight_Workshopproject
    }[pythonanywhere_username]()

    target_project.set_install_as_target_toggle(value=True)

    Sitedeployer(
        PATHFILE_deploypy=PATHFILE_deploypy,
        target_project=target_project
    ).Execute()

    logger.info('Deploy site!')
