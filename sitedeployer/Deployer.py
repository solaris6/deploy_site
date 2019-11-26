import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from sitedeployer._Sitetask.Sitetask import *
from sitedeployer.utils import log_environment
import shutil
import subprocess


class Deployer(
    Sitetask
):
    def __init__(self,
        PATHFILE_deploypy:Path=None,
        target_project:Projekt=None
    ):
        Sitetask.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )
        self._target_project = target_project

        self._target_project.attach_to_sitedeployer(
            sitedeployer=self
        )

    def pythonanywhere_username(self) -> str:
        return self.target_project().pythonanywhere_username()

    def target_project(self) -> Projekt:
        return self._target_project

    def Deploy(self) -> None:
        log_environment(logger=logger)

        logger.info(
'''# projekt:
target_project: '%target_project%'

# pythonanywhere:
pythonanywhere_username: '%pythonanywhere_username%'
URL_pythonanywhere_site: '%URL_pythonanywhere_site%'

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
            .replace('%target_project%', str(self.target_project()))
            \
            .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            .replace('%URL_pythonanywhere_site%', self.URL_pythonanywhere_site())
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

        for projekt in self.projekts_all():
            projekt.uninstall_as_package()


        URL_github_projekt_repository = self.target_project().URLSSH_github_projekt_repository()

        PATHDIR_root_projektrepository = self.PATHDIR_root() / self.target_project().NAME()
        if not PATHDIR_root_projektrepository.is_dir():
            subprocess.run(
                ['git', 'clone', URL_github_projekt_repository],
                cwd=str(self.PATHDIR_root())
            )

        PATHfile_root_projektrepository_makepy = PATHDIR_root_projektrepository / 'make.py'
        subprocess.run(
            ['python3.6', PATHfile_root_projektrepository_makepy],
            cwd=PATHDIR_root_projektrepository
        )

        # wsgi.py:
        logger.info('Process wsgi.py...')
        logger.info(
'''PATHFILE_wsgipy=%PATHFILE_wsgipy%'''
            .replace('%PATHFILE_wsgipy%', str(self.PATHFILE_wsgipy()))
        )

        logger.info('Write wsgi.py file...')

        PATHFILE_VERSION_LOCATION = PATHDIR_root_projektrepository / 'VERSION_LOCATION'

        PATHFILE_VERSION = PATHDIR_root_projektrepository / Path(PATHFILE_VERSION_LOCATION.read_text())
        FCONTENT_VERSION_list = PATHFILE_VERSION.read_text().splitlines()

        ver_major = int(FCONTENT_VERSION_list[0])
        ver_minor = int(FCONTENT_VERSION_list[1])

        PATHDIR_root_out_projekt = self.PATHDIR_root() / \
            ('_out/Release/%NAME%-%major%.%minor%-lnx/_projekt'
             .replace('%NAME%', self.target_project().NAME())
             .replace('%major%', str(ver_major))
             .replace('%minor%', str(ver_minor))
             )

        wsgipy_template = \
'''import sys, os
from pathlib import Path

sys.path = ['%PATHDIR_root_out_projekt%'] + sys.path

from sitepub_%NAME%.Sitepubapp import flask_app as application'''

        wsgipy_fc = wsgipy_template\
            .replace('%PATHDIR_root_out_projekt%', str(PATHDIR_root_out_projekt))\
            .replace('%NAME%', self.target_project().NAME())

        self.PATHFILE_wsgipy().write_text(
            wsgipy_fc
        )

        logger.info('WSGIPY_FILE_BEGIN' + wsgipy_fc + 'WSGIPY_FILE_END')
        logger.info('Write wsgi.py file!')
        logger.info('Process wsgi.py!')

        # update.py:
        logger.info('Write update.py file...')
        logger.info(
'''update.py paths:
PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy=%PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy%
PATHFILE_home_pythonanywhereusername_updatepy=%PATHFILE_home_pythonanywhereusername_updatepy%'''
            .replace('%PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy%', str(self.PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy()))
            .replace('%PATHFILE_home_pythonanywhereusername_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_updatepy()))
        )

        shutil.copyfile(
            self.PATHFILE_root_sitedeployer_sitedeployerpackage_updatepy(),
            self.PATHFILE_home_pythonanywhereusername_updatepy()
        )
        logger.info('Write update.py file!')