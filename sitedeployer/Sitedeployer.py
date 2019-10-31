import logging
import subprocess

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from typing import List, Type
import shutil
from pathlib import Path

from sitedeployer.utils import log_environment

from sitedeployer.Projekt._Projekt.Projekt import Projekt

from sitedeployer.Projekt.Project.Ln_Project import Ln_Project
from sitedeployer.Projekt.Project.ynsbase_Project import ynsbase_Project
from sitedeployer.Projekt.Project.ynsbasedata_Project import ynsbasedata_Project
from sitedeployer.Projekt.Project.cgbase_Project import cgbase_Project
from sitedeployer.Projekt.Project.fw_Project import fw_Project
from sitedeployer.Projekt.Project.myrta_Project import myrta_Project
from sitedeployer.Projekt.Project.projekt_Project import projekt_Project
from sitedeployer.Projekt.Project.rs_Project import rs_Project
from sitedeployer.Projekt.Project.rsdata_Project import rsdata_Project
from sitedeployer.Projekt.Project.sc_Project import sc_Project
from sitedeployer.Projekt.Project.skfb_Project import skfb_Project
from sitedeployer.Projekt.Project.sola_Project import sola_Project
from sitedeployer.Projekt.Project.una_Project import una_Project
from sitedeployer.Projekt.Workshop.ynsight_Workshop import ynsight_Workshop

class Sitedeployer:
    def __init__(self,
        PATHFILE_deploypy:Path=None,
        target_project:Projekt=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy
        self._target_project = target_project

    def projekts_Types_all(self) -> List[Type[Projekt]]:
        return [
            ynsbase_Project,
            ynsbasedata_Project,
            projekt_Project,
            myrta_Project,
            una_Project,
            rs_Project,
            rsdata_Project,
            sc_Project,
            skfb_Project,
            fw_Project,
            sola_Project,
            Ln_Project,
            cgbase_Project,

            ynsight_Workshop
        ]

    # projekt:
    def target_project(self) -> Projekt:
        return self._target_project

    # pythonanywhere:
    def pythonanywhere_username(self) -> str:
        return self.target_project().pythonanywhere_username()

    def URL_pythonanywhere_site(self) -> str:
        return self.pythonanywhere_username() + '.pythonanywhere.com'

    # github:
    def github_username(self) -> str:
        return 'ynsight'

    def python_version_list(self) -> List[int]:
        return [3, 6]

    def python_version_dot_str(self) -> str:
        python_version_list_str = []
        for version_comp_int in self.python_version_list():
            python_version_list_str.append(str(version_comp_int))
        return '.'.join(python_version_list_str)

    def python_version_solid_str(self) -> str:
        python_version_list_str = []
        for version_comp_int in self.python_version_list():
            python_version_list_str.append(str(version_comp_int))
        return ''.join(python_version_list_str)

    def FILENAME_python(self) -> str:
        return 'python%python_version_dot_str%'\
            .replace('%python_version_dot_str%', self.python_version_dot_str())

    def DIRNAME_venv(self) -> str:
        return 'python%python_version_solid_str%venv'\
            .replace('%python_version_solid_str%', self.python_version_solid_str())

    def DIRNAME_python(self) -> str:
        return 'python%python_version_dot_str%'\
            .replace('%python_version_dot_str%', self.python_version_dot_str())

    def PATHDIR_venvsitepackages(self) -> Path:
        return Path(
            '/home/%pythonanywhere_username%/.virtualenvs/%DIRNAME_venv%/lib/%DIRNAME_python%/site-packages'
                .replace('%pythonanywhere_username%', self.pythonanywhere_username())
                .replace('%DIRNAME_venv%', self.DIRNAME_venv())
                .replace('%DIRNAME_python%', self.DIRNAME_python())
        )

    def PATHDIR_venvbin(self) -> Path:
        return Path(
            '/home/%pythonanywhere_username%/.virtualenvs/%DIRNAME_venv%/bin'
                .replace('%pythonanywhere_username%', self.pythonanywhere_username())
                .replace('%DIRNAME_venv%', self.DIRNAME_venv())
        )

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

        for projekt_Type in self.projekts_Types_all():
            projekt = projekt_Type()
            projekt.attach_to_sitedeployer(
                sitedeployer=self
            )
            projekt.uninstall_as_package()
        self.target_project().attach_to_sitedeployer(
            sitedeployer=self
        )

        self.target_project().upload_on_pypi()


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

        PATHFILE_VERSION = PATHDIR_root_projektrepository / 'VERSION'
        FCONTENT_VERSION_list = PATHFILE_VERSION.read_text().splitlines()

        ver_major = int(FCONTENT_VERSION_list[0])
        ver_minor = int(FCONTENT_VERSION_list[1])

        PATHDIR_root_out_sitepub = self.PATHDIR_root() / \
            ('_out/Release/%NAME%-%major%.%minor%-lnx/_projekt/projectsitepub_%NAME%'
             .replace('%NAME%', self.target_project().NAME())
             .replace('%major%', str(ver_major))
             .replace('%minor%', str(ver_minor))
             )

        wsgipy_template = \
'''import sys, os
from pathlib import Path

sys.path = ['%PATHDIR_root_out_sitepub%'] + sys.path

from %projektsitepub_package%.flask_app import app as application
'''

        wsgipy_fc = wsgipy_template\
            .replace('%%PATHDIR_root_out_sitepub%%', str(PATHDIR_root_out_sitepub))\
            .replace('%projektsitepub_package%', self.target_project().projektsitepub_package())

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
