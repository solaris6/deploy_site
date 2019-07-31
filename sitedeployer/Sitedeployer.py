import logging
from typing import List

from sitedeployer.projects.core.Projektproject import Projektproject

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

import os
import shutil
from copy import copy
from pathlib import Path

from sitedeployer.projects.core.Project import Project
from sitedeployer.projects.core.Workshopproject import Workshopproject
from sitedeployer.utils import log_environment

class Sitedeployer:
    def __init__(self,
        PATHFILE_deploypy:Path=None,
        target_project:Project=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy
        self._target_project = target_project

        self._projects_all = []

        self._PATH_old = None
        self._PYTHONPATH_old = None

    # project:
    def target_project(self) -> Project:
        return self._target_project

    def projects_all(self) -> List[Project]:
        return self._projects_all

    # pythonanywhere:
    def pythonanywhere_username(self) -> str:
        return self.target_project().pythonanywhere_username()

    def URL_site(self) -> str:
        return self.pythonanywhere_username() + '.pythonanywhere.com'

    # github:
    def github_username(self) -> str:
        return 'ynsight'

    # PATHS:
    def PATHDIR_home_pythonanywhereusername(self) -> Path:
        return self.PATHDIR_root().parent

    def PATHDIR_root(self) -> Path:
        return self._PATHFILE_deploypy.parent.parent

    def PATHDIR_root_instemp(self) -> Path:
        return self.PATHDIR_root() / '_instemp'

    def PATHDIR_root_sitedeployer(self) -> Path:
        return self.PATHDIR_root_sitedeployer_sitedeployerpackage().parent

    def PATHDIR_root_sitedeployer_sitedeployerpackage(self) -> Path:
        return self.PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy().parent

    def PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy(self) -> Path:
        return self._PATHFILE_deploypy

    def PATHFILE_wsgipy(self) -> Path:
        return Path(
                '/var/www/%pythonanywhere_username%_pythonanywhere_com_wsgi.py'
                    .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            )

    def PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy(self) -> Path:
        return self.PATHDIR_root_sitedeployer_sitedeployerpackage() / 'update.py'

    def PATHFILE_home_pythonanywhereusername_updatepy(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername() / 'update.py'


    def Execute(self) -> None:
        for project_Type in self.target_project().dependencies_Types_all():
            if not project_Type is type(self.target_project()):
                self._projects_all.append(
                    project_Type()
                )

        self._projects_all += [self.target_project()]

        for project in self.projects_all():
            project.attach_to_sitedeployer(
                sitedeployer=self
            )
            project.Init()

        for project in self.projects_all():
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
                project.set_install_as_projektcard_toggle(
                    value=True
                )

        log_environment(logger=logger)


        logger.info('Process common...')
        logger.info(
'''# project:
target_project: '%target_project%'
projects_all: '%projects_all%'

# pythonanywhere:
pythonanywhere_username: '%pythonanywhere_username%'
URL_site: '%URL_site%'

# github:
github_username: '%github_username%'

# paths:
PATHDIR_home_pythonanywhereusername: '%PATHDIR_home_pythonanywhereusername%'
PATHDIR_root: '%PATHDIR_root%'
PATHDIR_root_instemp: '%PATHDIR_root_instemp%'
PATHDIR_root_sitedeployer: '%PATHDIR_root_sitedeployer%'
PATHDIR_root_sitedeployer_sitedeployerpackage: '%PATHDIR_root_sitedeployer_sitedeployerpackage%'
PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy: '%PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy%'
PATHFILE_wsgipy: '%PATHFILE_wsgipy%'
PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy: '%PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy%'
PATHFILE_home_pythonanywhereusername_updatepy: '%PATHFILE_home_pythonanywhereusername_updatepy%'
'''
            .replace('%target_project%', str(self.target_project()))
            .replace('%projects_all%', str(self.projects_all()))
            \
            .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            .replace('%URL_site%', self.URL_site())
            \
            .replace('%github_username%', self.github_username())
            \
            .replace('%PATHDIR_home_pythonanywhereusername%', str(self.PATHDIR_home_pythonanywhereusername()))
            .replace('%PATHDIR_root%', str(self.PATHDIR_root()))
            .replace('%PATHDIR_root_instemp%', str(self.PATHDIR_root_instemp()))
            .replace('%PATHDIR_root_sitedeployer%', str(self.PATHDIR_root_sitedeployer()))
            .replace('%PATHDIR_root_sitedeployer_sitedeployerpackage%', str(self.PATHDIR_root_sitedeployer_sitedeployerpackage()))
            .replace('%PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy%', str(self.PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy()))
            .replace('%PATHFILE_wsgipy%', str(self.PATHFILE_wsgipy()))
            .replace('%PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy%', str(self.PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy()))
            .replace('%PATHFILE_home_pythonanywhereusername_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_updatepy()))
        )

        logger.info('Make common dirs...')
        self.PATHDIR_root_instemp().mkdir(parents=True)
        logger.info('Make common dirs!')
        logger.info('Process common!')

        log_environment(logger=logger)
        self._PATH_old = copy(os.environ['PATH']) if 'PATH' in os.environ else ''
        self._PYTHONPATH_old = copy(os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else ''
        log_environment(logger=logger)


        logger.info('Process temp dependencies...')
        for project in self.projects_all():
            if not isinstance(project, Workshopproject) and project.install_as_temp_toggle():
                project.install_as_temp()
        logger.info('Process temp dependencies!')


        logger.info('Process lib/projektcard dependencies...')
        for project in self.projects_all():
            if not project is self.target_project():
                if project.install_as_lib_toggle() and project.install_as_projektcard_toggle():
                    project.install_as_lib_and_projektcard()

                elif project.install_as_lib_toggle():
                    project.install_as_lib()

                elif project.install_as_projektcard_toggle():
                    project.install_as_projektcard()
        logger.info('Process lib/projektcard dependencies!')

        if self.target_project().install_as_target_toggle():
            self.target_project().install_as_target()

        # wsgi.py:
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

# projects entries:
%projects_entries%

from %projektorworkshopsitepub_package%.flask_app import app as application
'''

        projects_entries = ''
        for i,project in enumerate(self.projects_all()):
            projects_entries += ('' if i==0 else '\n\n') + '# ' + project.report() + ':\n' + project.wsgipy_entry()

        wsgipy_fc = wsgipy_template\
            .replace('%projects_entries%', projects_entries)\
            .replace('%projektorworkshopsitepub_package%', self.target_project().projektorworkshopsitepub_package())

        self.PATHFILE_wsgipy().write_text(
            wsgipy_fc
        )

        logger.info('WSGIPY_FILE_BEGIN' + wsgipy_fc + 'WSGIPY_FILE_END')
        logger.info('Write wsgi.py file!')
        logger.info('Process wsgi.py!')


        log_environment(logger=logger)
        os.environ['PATH'] = self._PATH_old
        os.environ['PYTHONPATH'] = self._PYTHONPATH_old
        log_environment(logger=logger)


        # update.py:
        logger.info('Process update.py...')
        logger.info(
'''update.py paths:
PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy=%PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy%
PATHFILE_home_pythonanywhereusername_updatepy=%PATHFILE_home_pythonanywhereusername_updatepy%'''
            .replace('%PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy%', str(self.PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy()))
            .replace('%PATHFILE_home_pythonanywhereusername_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_updatepy()))
        )

        logger.info('Write update.py file...')
        shutil.copyfile(
            self.PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy(),
            self.PATHFILE_home_pythonanywhereusername_updatepy()
        )
        logger.info('Write update.py file!')
        logger.info('Process update.py!')
