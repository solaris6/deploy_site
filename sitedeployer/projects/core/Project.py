import json
import os
import platform
import shutil, subprocess
import sys
from copy import copy
from pathlib import Path
from typing import Type, List, Dict, Any

import logging

from sitedeployer.utils import remove_duplicates

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[sitedeployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

class Project:
    def __init__(self):
        self._install_as__target_toggle = False
        self._is_installed_as__target = False

        self._PATH_old = None
        self._PYTHONPATH_old = None
        self._sitedeployer = None

        self._wsgipy_entry = ''

    def attach_to_sitedeployer(self,
        sitedeployer:'Sitedeployer'=None
    ) -> None:
        self._sitedeployer = sitedeployer

    def sitedeployer(self) -> 'Sitedeployer':
        return self._sitedeployer


    def Init(self) -> None:
        logger.info('Init Project...')
        logger.info(
'''# names:
NAME: '%NAME%'
projektorworkshopsitepub_package: '%projektorworkshopsitepub_package%'
projektorworkshop_package: '%projektorworkshop_package%'
projektorworkshop: '%projektorworkshop%'


# PATHS:
PATHDIR_root: '%PATHDIR_root%'
PATHDIR_root_instemp: '%PATHDIR_root_instemp%'
PATHDIR_root_projectrepository: '%PATHDIR_root_projectrepository%'
PATHDIR_root_instemp_project: '%PATHDIR_root_instemp_project%'
PATHDIR_root_out_proojektorworkshop: '%PATHDIR_root_out_proojektorworkshop%'


# github:
github_username: '%github_username%'
github_url_type: '%github_url_type%'
URLSSH_github_project_repository: '%URLSSH_github_project_repository%'
URLHTTP_github_project_repository: '%URLHTTP_github_project_repository%'
URLHTTPS_github_project_repository: '%URLHTTPS_github_project_repository%'
URL_github_project_repository: '%URL_github_project_repository%'

# pythonanywhere:
pythonanywhere_username: '%pythonanywhere_username%'

# dependencies:
dependencies_lib_specific_deployer_Types: '%dependencies_lib_specific_deployer_Types%'
dependencies_Types_all: '%dependencies_Types_all%'
dependencies_lib_common_deployer_Types: '%dependencies_lib_common_deployer_Types%'
dependencies_lib_specific_deployer_Types_all: '%dependencies_lib_specific_deployer_Types_all%'
dependencies_lib_temp_deployer_Types: '%dependencies_lib_temp_deployer_Types%'
'''
            .replace('%NAME%', self.NAME())
            .replace('%projektorworkshopsitepub_package%', self.projektorworkshopsitepub_package())
            .replace('%projektorworkshop_package%', self.projektorworkshop_package())
            .replace('%projektorworkshop%', self.projektorworkshop())
            \
            .replace('%PATHDIR_root%', str(self.PATHDIR_root()))
            .replace('%PATHDIR_root_instemp%', str(self.PATHDIR_root_instemp()))
            .replace('%PATHDIR_root_projectrepository%', str(self.PATHDIR_root_projectrepository()))
            .replace('%PATHDIR_root_instemp_project%', str(self.PATHDIR_root_instemp_project()))
            .replace('%PATHDIR_root_out_proojektorworkshop%', str(self.PATHDIR_root_out_proojektorworkshop()))
            \
            .replace('%github_username%', self.github_username())
            .replace('%github_url_type%', self.github_url_type())
            .replace('%URLSSH_github_project_repository%', self.URLSSH_github_project_repository())
            .replace('%URLHTTP_github_project_repository%', self.URLHTTP_github_project_repository())
            .replace('%URLHTTPS_github_project_repository%', self.URLHTTPS_github_project_repository())
            .replace('%URL_github_project_repository%', self.URL_github_project_repository())
            \
            .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            \
            .replace('%dependencies_lib_specific_deployer_Types%', str(self.dependencies_lib_specific_deployer_Types()))
            .replace('%dependencies_Types_all%', str(self.dependencies_Types_all()))
            .replace('%dependencies_lib_common_deployer_Types%', str(self.dependencies_lib_common_deployer_Types()))
            .replace('%dependencies_lib_specific_deployer_Types_all%', str(self.dependencies_lib_specific_deployer_Types_all()))
            .replace('%dependencies_lib_temp_deployer_Types%', str(self.dependencies_lib_temp_deployer_Types()))
        )

        logger.info('Init Project!')


    # names:
    def NAME(self) -> str:
        raise NotImplementedError("")

    def projektorworkshopsitepub_package(self) -> str:
        return '%projektorworkshop%sitepub_%NAME%'\
            .replace('%projektorworkshop%', self.projektorworkshop())\
            .replace('%NAME%', self.NAME())

    def projektorworkshop_package(self) -> str:
        return '%projektorworkshop%_%NAME%'\
            .replace('%projektorworkshop%', self.projektorworkshop())\
            .replace('%NAME%', self.NAME())

    def projektorworkshop(self) -> str:
        raise NotImplementedError("")


    # PATHS:
    def PATHDIR_root(self) -> Path:
        return self.sitedeployer().PATHDIR_root()

    def PATHDIR_root_instemp(self) -> Path:
        return self.sitedeployer().PATHDIR_root_instemp()

    def PATHDIR_root_projectrepository(self) -> Path:
        return self.PATHDIR_root() / self.NAME()

    def PATHDIR_root_instemp_project(self) -> Path:
        return self.PATHDIR_root_instemp() / self.NAME()

    def PATHDIR_root_out_proojektorworkshop(self) -> Path:
        return self.PATHDIR_root() / '_out/Release/%NAME%/_2019_2_0/_%projektorworkshop%'\
            .replace('%NAME%', self.NAME())\
            .replace('%projektorworkshop%', self.projektorworkshop())


    # github:
    def github_username(self) -> str:
        return self.sitedeployer().github_username()

    def github_url_type(self) -> str:
        raise NotImplementedError("")

    def URLSSH_github_project_repository(self) -> str:
        return '''git@github.com:%github_username%/%NAME%.git''' \
            .replace('%NAME%', self.NAME()) \
            .replace('%github_username%', self.github_username())

    def URLHTTP_github_project_repository(self) -> str:
        return '''http://github.com/%github_username%/%NAME%.git''' \
            .replace('%NAME%', self.NAME()) \
            .replace('%github_username%', self.github_username())

    def URLHTTPS_github_project_repository(self) -> str:
        return '''https://github.com/%github_username%/%NAME%.git''' \
            .replace('%NAME%', self.NAME()) \
            .replace('%github_username%', self.github_username())

    def URL_github_project_repository(self) -> str:
        result = None
        if self.github_url_type() == 'ssh':
            result = self.URLSSH_github_project_repository()
        elif self.github_url_type() == 'http':
            result = self.URLHTTP_github_project_repository()
        elif self.github_url_type() == 'https':
            result = self.URLHTTPS_github_project_repository()
        return result


    # pythonanywhere:
    def pythonanywhere_username(self) -> str:
        raise NotImplementedError("")


    # dependencies:
    #   temp:
    def dependencies_lib_temp_deployer_Types(self) -> List[Type['Project']]:
        return self.dependencies_lib_common_deployer_Types()

    #   deployer:
    def dependencies_lib_common_deployer_Types(self) -> List[Type['Project']]:
        from sitedeployer.projects.builtin.projekt.base_Projektproject import base_Projektproject
        from sitedeployer.projects.builtin.projekt.projekt_Projektproject import projekt_Projektproject
        from sitedeployer.projects.builtin.projekt.myrta_Projektproject import myrta_Projektproject
        return [
            base_Projektproject,
            projekt_Projektproject,
            myrta_Projektproject
        ]

    def dependencies_lib_specific_deployer_Types(self) -> List[Type['Project']]:
        raise NotImplementedError("")

    def dependencies_lib_specific_deployer_Types_all(self) -> List[Type['Project']]:
        return remove_duplicates(self.dependencies_lib_common_deployer_Types() + self.dependencies_lib_specific_deployer_Types())


    #   site:
    def dependencies_lib_common_site_Types(self) -> List[Type['Project']]:
        from sitedeployer.projects.builtin.projekt.base_Projektproject import base_Projektproject
        from sitedeployer.projects.builtin.projekt.projekt_Projektproject import projekt_Projektproject
        from sitedeployer.projects.builtin.projekt.myrta_Projektproject import myrta_Projektproject
        return [
            base_Projektproject,
            projekt_Projektproject,
            myrta_Projektproject
        ]

    def dependencies_lib_specific_site_Types(self) -> List[Type['Project']]:
        raise NotImplementedError("")

    def dependencies_lib_specific_site_Types_all(self) -> List[Type['Project']]:
        return remove_duplicates(self.dependencies_lib_common_site_Types() + self.dependencies_lib_specific_site_Types())



    #   all:
    def dependencies_lib_Types_all(self) -> List[Type['Project']]:
        return remove_duplicates(self.dependencies_lib_specific_deployer_Types_all() + self.dependencies_lib_specific_site_Types_all())

    def dependencies_Types_all(self) -> List[Type['Project']]:
        raise NotImplementedError("")




    # build:
    def clone_project(self) -> None:
        logger.info('Clone "%project%" repository...'.replace('%project%', self.NAME()))
        if not self.PATHDIR_root_projectrepository().is_dir():
            subprocess.run(
                ['git', 'clone', self.URL_github_project_repository()],
                cwd=str(self.PATHDIR_root())
            )
            logger.info('Clone "%project%" repository!'.replace('%project%', self.NAME()))
        else:
            logger.info('Cloned "%project%" already exists, skipped...'.replace('%project%', self.NAME()))

    def wsgipy_entry(self) -> str:
        return self._wsgipy_entry

    # as target:
    def set_install_as__target_toggle(self,
        value:bool=None
    ) -> None:
        self._install_as__target_toggle = value

    def install_as__target_toggle(self) -> bool:
        return self._install_as__target_toggle

    def is_installed_as__target(self) -> bool:
        return self._is_installed_as__target

    def install_as__target(self) -> None:
        raise NotImplementedError("")


    def report(self) -> str:
        raise NotImplementedError("")