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

class Projekt:
    def __init__(self):
        self._toggle_install_as__target = False
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
        logger.info('Init Projekt...')
        logger.info(
'''# names:
NAME: '%NAME%'
projektsitepub_package: '%projektsitepub_package%'
projekt_package: '%projekt_package%'
projekt: '%projekt%'


# PATHS:
PATHDIR_root: '%PATHDIR_root%'
PATHDIR_root_projektrepository: '%PATHDIR_root_projektrepository%'
PATHDIR_root_out_projekt: '%PATHDIR_root_out_projekt%'


# github:
github_username: '%github_username%'
github_url_type: '%github_url_type%'
URLSSH_github_projekt_repository: '%URLSSH_github_projekt_repository%'
URLHTTP_github_projekt_repository: '%URLHTTP_github_projekt_repository%'
URLHTTPS_github_projekt_repository: '%URLHTTPS_github_projekt_repository%'
URL_github_projekt_repository: '%URL_github_projekt_repository%'

# pythonanywhere:
pythonanywhere_username: '%pythonanywhere_username%'

# dependencies:
dependencies_Types: '%dependencies_Types%'
'''
            .replace('%NAME%', self.NAME())
            .replace('%projektsitepub_package%', self.projektsitepub_package())
            .replace('%projekt_package%', self.projekt_package())
            .replace('%projekt%', self.projekt())
            \
            .replace('%PATHDIR_root%', str(self.PATHDIR_root()))
            .replace('%PATHDIR_root_projektrepository%', str(self.PATHDIR_root_projektrepository()))
            .replace('%PATHDIR_root_out_projekt%', str(self.PATHDIR_root_out_projekt()))
            \
            .replace('%github_username%', self.github_username())
            .replace('%github_url_type%', self.github_url_type())
            .replace('%URLSSH_github_projekt_repository%', self.URLSSH_github_projekt_repository())
            .replace('%URLHTTP_github_projekt_repository%', self.URLHTTP_github_projekt_repository())
            .replace('%URLHTTPS_github_projekt_repository%', self.URLHTTPS_github_projekt_repository())
            .replace('%URL_github_projekt_repository%', self.URL_github_projekt_repository())
            \
            .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            \
            .replace('%dependencies_Types%', str(self.dependencies_Types()))
        )

        logger.info('Init Projekt!')


    # names:
    def NAME(self) -> str:
        raise NotImplementedError("")

    def projektsitepub_package(self) -> str:
        return '%projekt%sitepub_%NAME%'\
            .replace('%projekt%', self.projekt())\
            .replace('%NAME%', self.NAME())

    def projekt_package(self) -> str:
        return '%projekt%_%NAME%'\
            .replace('%projekt%', self.projekt())\
            .replace('%NAME%', self.NAME())

    def projekt(self) -> str:
        raise NotImplementedError("")


    # PATHS:
    def PATHDIR_root(self) -> Path:
        return self.sitedeployer().PATHDIR_root()

    def PATHDIR_root_projektrepository(self) -> Path:
        return self.PATHDIR_root() / self.NAME()

    def PATHDIR_root_out_projekt(self) -> Path:
        return self.PATHDIR_root() / '_out/Release/%NAME%/_2019_2_0/_projekt'\
            .replace('%NAME%', self.NAME())


    # github:
    def github_username(self) -> str:
        return self.sitedeployer().github_username()

    def github_url_type(self) -> str:
        raise NotImplementedError("")

    def URLSSH_github_projekt_repository(self) -> str:
        return '''git@github.com:%github_username%/%NAME%.git''' \
            .replace('%NAME%', self.NAME()) \
            .replace('%github_username%', self.github_username())

    def URLHTTP_github_projekt_repository(self) -> str:
        return '''http://github.com/%github_username%/%NAME%.git''' \
            .replace('%NAME%', self.NAME()) \
            .replace('%github_username%', self.github_username())

    def URLHTTPS_github_projekt_repository(self) -> str:
        return '''https://github.com/%github_username%/%NAME%.git''' \
            .replace('%NAME%', self.NAME()) \
            .replace('%github_username%', self.github_username())

    def URL_github_projekt_repository(self) -> str:
        result = None
        if self.github_url_type() == 'ssh':
            result = self.URLSSH_github_projekt_repository()
        elif self.github_url_type() == 'http':
            result = self.URLHTTP_github_projekt_repository()
        elif self.github_url_type() == 'https':
            result = self.URLHTTPS_github_projekt_repository()
        return result


    # pythonanywhere:
    def pythonanywhere_username(self) -> str:
        raise NotImplementedError("")


    # dependencies:
    #   site:

    def dependencies_Types(self) -> List[Type['Projekt']]:
        from sitedeployer.projects.builtin.project.base_Project import base_Project
        from sitedeployer.projects.builtin.project.projekt_Project import projekt_Project
        return [
            base_Project,
            projekt_Project
        ]


    # build:
    def clone_projekt(self) -> None:
        logger.info('Clone "%projekt%" repository...'.replace('%projekt%', self.NAME()))
        if not self.PATHDIR_root_projektrepository().is_dir():
            subprocess.run(
                ['git', 'clone', self.URL_github_projekt_repository()],
                cwd=str(self.PATHDIR_root())
            )
            logger.info('Clone "%projekt%" repository!'.replace('%projekt%', self.NAME()))
        else:
            logger.info('Cloned "%projekt%" already exists, skipped...'.replace('%projekt%', self.NAME()))

    def wsgipy_entry(self) -> str:
        return self._wsgipy_entry

    # as target:
    def set_toggle_install_as__target(self,
        value:bool=None
    ) -> None:
        self._toggle_install_as__target = value

    def toggle_install_as__target(self) -> bool:
        return self._toggle_install_as__target

    def is_installed_as__target(self) -> bool:
        return self._is_installed_as__target

    def install_as__target(self) -> None:
        raise NotImplementedError("")

    def install(self) -> None:
        raise NotImplementedError("")


    def report(self) -> str:
        raise NotImplementedError("")