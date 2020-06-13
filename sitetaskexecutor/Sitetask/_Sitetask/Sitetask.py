import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[task] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from typing import List, Type
from pathlib import Path

import json
import os
import subprocess
from sitetaskexecutor.Gitproject._Gitproject.Gitproject import Gitproject

from sitetaskexecutor.Gitproject.una_Gitproject import una_Gitproject
from sitetaskexecutor.Gitproject.Ln_Gitproject import Ln_Gitproject
from sitetaskexecutor.Gitproject.agent_Gitproject import agent_Gitproject
from sitetaskexecutor.Gitproject.fw_Gitproject import fw_Gitproject
from sitetaskexecutor.Gitproject.letters_Gitproject import letters_Gitproject
from sitetaskexecutor.Gitproject.myrta_Gitproject import myrta_Gitproject
from sitetaskexecutor.Gitproject.projekt_Gitproject import projekt_Gitproject
from sitetaskexecutor.Gitproject.rs_Gitproject import rs_Gitproject
from sitetaskexecutor.Gitproject.rsdata_Gitproject import rsdata_Gitproject
from sitetaskexecutor.Gitproject.sc_Gitproject import sc_Gitproject
from sitetaskexecutor.Gitproject.skfb_Gitproject import skfb_Gitproject
from sitetaskexecutor.Gitproject.sola_Gitproject import sola_Gitproject
from sitetaskexecutor.Gitproject.ynsbase_Gitproject import ynsbase_Gitproject
from sitetaskexecutor.Gitproject.ynsight_Gitproject import ynsight_Gitproject

class Sitetask:

    @staticmethod
    def log_environment() -> None:
        environment_report_dict = {}

        environment_report_dict['cwd'] = os.getcwd()

        if 'PATH' in os.environ:
            environment_report_dict['PATH'] = os.environ['PATH'].split(os.pathsep)
        else:
            environment_report_dict['PATH'] = []

        if 'PYTHONPATH' in os.environ:
            environment_report_dict['PYTHONPATH'] = os.environ['PYTHONPATH'].split(os.pathsep)
        else:
            environment_report_dict['PYTHONPATH'] = []

        logger.info(
            json.dumps(
                {
                    'environment_report': environment_report_dict
                },
                indent=2
            )
        )

    @staticmethod
    def projekts_Types_all() -> List[Type[Gitproject]]:
        return [
            agent_Gitproject,
            ynsbase_Gitproject,
            letters_Gitproject,
            projekt_Gitproject,
            myrta_Gitproject,
            una_Gitproject,
            rs_Gitproject,
            rsdata_Gitproject,
            sc_Gitproject,
            skfb_Gitproject,
            fw_Gitproject,
            sola_Gitproject,
            Ln_Gitproject,

            ynsight_Gitproject
        ]


    def __init__(self,
        PATHFILE_executetaskpy:Path=None
    ):
        self._PATHFILE_executetaskpy = PATHFILE_executetaskpy

        self._projekts_list = []
        for projekt_Type in self.projekts_Types_all():
            projekt = projekt_Type()
            projekt.attach_to_task(
                task=self
            )
            self._projekts_list.append(projekt)

        PATHFILE_YNSIGHT_GITHUB_TOKEN_txt = PATHFILE_executetaskpy.parent.parent.parent / 'YNSIGHT_GITHUB_TOKEN.txt'
        if PATHFILE_YNSIGHT_GITHUB_TOKEN_txt.is_file():
            YNSIGHT_GITHUB_TOKEN = PATHFILE_YNSIGHT_GITHUB_TOKEN_txt.read_text()
            os.environ['YNSIGHT_GITHUB_TOKEN'] = YNSIGHT_GITHUB_TOKEN


    def NAME(self) -> str:
        return self.__class__.__name__[:-5]


    # pythonanywhere:
    def projekts_all(self) -> List[Gitproject]:
        return self._projekts_list

    def pythonanywhere_username(self) -> str:
        raise NotImplementedError

    def URL_pythonanywhere_site(self) -> str:
        return self.pythonanywhere_username() + '.pythonanywhere.com'


    # github:
    def github_username(self) -> str:
        return 'ynsight'


    # python:
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
        return self._PATHFILE_executetaskpy.parent.parent

    def PATHDIR_root_sitetask(self) -> Path:
        return self.PATHDIR_root_sitetask_sitetaskpackage().parent

    def PATHDIR_root_sitetask_sitetaskpackage(self) -> Path:
        return self.PATHFILE_root_sitetask_sitetaskpackage_executetaskpy().parent


    def PATHFILE_root_sitetask_sitetaskpackage_executetaskpy(self) -> Path:
        return self._PATHFILE_executetaskpy


    def PATHFILE_root_sitetask_sitetaskpackage_updatepy(self) -> Path:
        return self.PATHDIR_root_sitetask_sitetaskpackage() / 'update.py'

    def PATHFILE_home_pythonanywhereusername_updatepy(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername() / 'update.py'


    def Execute(self) -> bool:
        pass

    def _Execute(self) -> bool:
        logger.info('Executing "%NAME%" task...'.replace('%NAME%', self.NAME()))
        self.log_environment()

        self.Execute()

        logger.info('Executed "%NAME%" task!'.replace('%NAME%', self.NAME()))