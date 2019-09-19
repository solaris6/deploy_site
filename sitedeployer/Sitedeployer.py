import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from typing import List

from sitedeployer.projects.core.Project import Project
import os
import shutil
from copy import copy
from pathlib import Path

from sitedeployer.projects.core.Projekt import Projekt
from sitedeployer.projects.core.Workshop import Workshop
from sitedeployer.utils import log_environment

class Sitedeployer:
    def __init__(self,
        PATHFILE_deploypy:Path=None,
        target_projekt:Projekt=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy
        self._target_projekt = target_projekt

        self._projekts_all = []

        self._PATH_old = None
        self._PYTHONPATH_old = None

    # projekt:
    def target_projekt(self) -> Projekt:
        return self._target_projekt

    def projekts_all(self) -> List[Projekt]:
        return self._projekts_all

    # pythonanywhere:
    def pythonanywhere_username(self) -> str:
        return self.target_projekt().pythonanywhere_username()

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
        for projekt_Type in self.target_projekt().dependencies_Types():
            if not projekt_Type is type(self.target_projekt()):
                self._projekts_all.append(
                    projekt_Type()
                )

        self._projekts_all += [self.target_projekt()]

        for projekt in self.projekts_all():
            projekt.attach_to_sitedeployer(
                sitedeployer=self
            )
            projekt.Init()

        for projekt in self.projekts_all():
            if type(projekt) in self.target_projekt().dependencies_Types():
                projekt.set_toggle_install_as__dependency(
                    value=True
                )

        log_environment(logger=logger)


        logger.info('Process common...')
        logger.info(
'''# projekt:
target_projekt: '%target_projekt%'
projekts_all: '%projekts_all%'

# pythonanywhere:
pythonanywhere_username: '%pythonanywhere_username%'
URL_site: '%URL_site%'

# github:
github_username: '%github_username%'

# paths:
PATHDIR_home_pythonanywhereusername: '%PATHDIR_home_pythonanywhereusername%'
PATHDIR_root: '%PATHDIR_root%'
PATHDIR_root_sitedeployer: '%PATHDIR_root_sitedeployer%'
PATHDIR_root_sitedeployer_sitedeployerpackage: '%PATHDIR_root_sitedeployer_sitedeployerpackage%'
PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy: '%PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy%'
PATHFILE_wsgipy: '%PATHFILE_wsgipy%'
PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy: '%PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy%'
PATHFILE_home_pythonanywhereusername_updatepy: '%PATHFILE_home_pythonanywhereusername_updatepy%'
'''
            .replace('%target_projekt%', str(self.target_projekt()))
            .replace('%projekts_all%', str(self.projekts_all()))
            \
            .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            .replace('%URL_site%', self.URL_site())
            \
            .replace('%github_username%', self.github_username())
            \
            .replace('%PATHDIR_home_pythonanywhereusername%', str(self.PATHDIR_home_pythonanywhereusername()))
            .replace('%PATHDIR_root%', str(self.PATHDIR_root()))
            .replace('%PATHDIR_root_sitedeployer%', str(self.PATHDIR_root_sitedeployer()))
            .replace('%PATHDIR_root_sitedeployer_sitedeployerpackage%', str(self.PATHDIR_root_sitedeployer_sitedeployerpackage()))
            .replace('%PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy%', str(self.PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy()))
            .replace('%PATHFILE_wsgipy%', str(self.PATHFILE_wsgipy()))
            .replace('%PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy%', str(self.PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy()))
            .replace('%PATHFILE_home_pythonanywhereusername_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_updatepy()))
        )

        logger.info('Process common!')

        log_environment(logger=logger)
        self._PATH_old = copy(os.environ['PATH']) if 'PATH' in os.environ else ''
        self._PYTHONPATH_old = copy(os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else ''
        log_environment(logger=logger)


        for projekt in self.projekts_all():
            projekt.install()

        self.target_projekt().install()

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

# projekts entries:
%projekts_entries%

from %projektsitepub_package%.flask_app import app as application
'''

        projekts_entries = ''
        for i,projekt in enumerate(self.projekts_all()):
            projekts_entries += ('' if i==0 else '\n\n') + '# ' + projekt.report() + ':\n' + projekt.wsgipy_entry()

        wsgipy_fc = wsgipy_template\
            .replace('%projekts_entries%', projekts_entries)\
            .replace('%projektsitepub_package%', self.target_projekt().projektsitepub_package())

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
