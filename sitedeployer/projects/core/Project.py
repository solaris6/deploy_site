import json
import os
import platform
import shutil, subprocess
import sys
from copy import copy
from pathlib import Path
from typing import Type, List, Dict, Any

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[sitedeployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

class Project:
    def __init__(self):
        self._install_as_target_toggle = False
        self._is_installed_as_target = False

        self._PATH_old = None
        self._PYTHONPATH_old = None
        self._sitedeployer = None

        self._wsgipy_entry = ''

#             projects_packages_syspaths_appends += ('' if i==0 else '\n') +\
# "os.environ['PATH'] += os.pathsep + '/home/%pythonanywhere_username%/root/ins/%dependency_NAME%/bin'"\
#     .replace('%dependency_NAME%', project_installed)
#
#             projects_packages_PATH_appends += ('' if i==0 else '\n') +\
# "sys.path = ['/home/%pythonanywhere_username%/root/ins/%dependency_NAME%/lib'] + sys.path"\
#     .replace('%dependency_NAME%', project_installed)

    def attach_to_sitedeployer(self,
        sitedeployer:'Sitedeployer'=None
    ) -> None:
        self._sitedeployer = sitedeployer

    def sitedeployer(self) -> 'Sitedeployer':
        return self._sitedeployer


    def PATHDIR_root(self) -> Path:
        return self.sitedeployer().PATHDIR_root()

    def PATHDIR_root_instemp(self) -> Path:
        return self.sitedeployer().PATHDIR_root_instemp()


    def NAME(self) -> str:
        raise NotImplementedError("")

    def pythonanywhere_username(self) -> str:
        raise NotImplementedError("")

    def github_username(self) -> str:
        return self.sitedeployer().github_username()

    def github_url_type(self) -> str:
        raise NotImplementedError("")

    def projektorworkshop_Type(self) -> str:
        raise NotImplementedError("")


    def PATHDIR_root_projectrepository(self) -> Path:
        return self.PATHDIR_root() / self.NAME()

    def PATHDIR_root_instemp_project(self) -> Path:
        return self.PATHDIR_root_instemp() / self.NAME()


    def is_installed(self) -> bool:
        raise NotImplementedError("")


    def set_install_as_target_toggle(self,
        value:bool=None
    ) -> None:
        self._install_as_target_toggle = value

    def install_as_target_toggle(self) -> bool:
        return self._install_as_target_toggle

    def is_installed_as_target(self) -> bool:
        return self._is_installed_as_target

    def install_as_target(self) -> None:
        raise NotImplementedError("")


    def dependencies_lib_self_Types(self) -> List[Type['Project']]:
        raise NotImplementedError("")

    def dependencies_Types_all(self) -> List[Type['Project']]:
        raise NotImplementedError("")

    def dependencies_lib_common_Types(self) -> List[Type['Project']]:
        from sitedeployer.projects.builtin.projekt.base_Projektproject import base_Projektproject
        from sitedeployer.projects.builtin.projekt.projekt_Projektproject import projekt_Projektproject
        from sitedeployer.projects.builtin.projekt.myrta_Projektproject import myrta_Projektproject
        return [
            base_Projektproject,
            projekt_Projektproject,
            myrta_Projektproject
        ]

    def dependencies_lib_Types_all(self) -> List[Type['Project']]:
        return self.dependencies_lib_common_Types() + self.dependencies_lib_self_Types()

    def dependencies_lib_temp_Types(self) -> List[Type['Project']]:
        return self.dependencies_lib_common_Types()



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

    def report(self) -> str:
        raise NotImplementedError("")