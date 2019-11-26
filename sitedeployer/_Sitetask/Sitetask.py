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
from pathlib import Path

from sitedeployer.Projekt._Projekt.Projekt import Projekt

from sitedeployer.Projekt.Project.Ln_Project import Ln_Project
from sitedeployer.Projekt.Project.ynsbase_Project import ynsbase_Project
from sitedeployer.Projekt.Project.ynsbasedata_Project import ynsbasedata_Project
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

class Sitetask:
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy

        self._projekts_list = []
        for projekt_Type in self.projekts_Types_all():
            projekt = projekt_Type()
            projekt.attach_to_sitedeployer(
                sitedeployer=self
            )
            self._projekts_list.append(projekt)

    # pythonanywhere:
    def projekts_all(self) -> List[Projekt]:
        return self._projekts_list

    # pythonanywhere:
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

            ynsight_Workshop
        ]

    def pythonanywhere_username(self) -> str:
        raise NotImplementedError

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
