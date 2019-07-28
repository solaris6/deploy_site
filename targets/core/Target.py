import json
import os
import platform
import shutil, subprocess
import sys
from copy import copy
from pathlib import Path
from typing import Type, List, Dict, Any

import logging

from utils import log_environment

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[sitedeployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

class Target:
    def __init__(self):
        self._PATH_old = None
        self._PYTHONPATH_old = None
        self._ynsight_projects_installed = []
        self._sitedeployer = None


    def attach_to_sitedeployer(self,
        sitedeployer:'Sitedeployer'=None
    ) -> None:
        self._sitedeployer = sitedeployer

    def sitedeployer(self) -> 'Sitedeployer':
        return self._sitedeployer


    def PATHDIR_root(self) -> Path:
        return self.sitedeployer().PATHDIR_root()

    def PATHDIR_root_ins(self) -> Path:
        return self.sitedeployer().PATHDIR_root_ins()

    def PATHDIR_root_instemp(self) -> Path:
        return self.sitedeployer().PATHDIR_root_ins()


    # temp ynsight dependencies:
    def temp_ynsight_dependencies(self) -> List[Type['Projekttarget']]:
        from targets.builtin.projekt.base_Projekttarget import base_Projekttarget
        from targets.builtin.projekt.projekt_Projekttarget import projekt_Projekttarget
        from targets.builtin.projekt.myrta_Projekttarget import myrta_Projekttarget
        return [
            base_Projekttarget,
            projekt_Projekttarget,
            myrta_Projekttarget
        ]


    # ynsight dependencies:
    def ynsight_dependencies_common(self) -> List[Type['Target']]:
        from targets.builtin.projekt.base_Projekttarget import base_Projekttarget
        from targets.builtin.projekt.projekt_Projekttarget import projekt_Projekttarget
        from targets.builtin.projekt.myrta_Projekttarget import myrta_Projekttarget
        return [
            base_Projekttarget,
            projekt_Projekttarget,
            myrta_Projekttarget
        ]

    def ynsight_dependencies_self(self) -> List[Type['Target']]:
        raise NotImplementedError("")

    def ynsight_dependencies_all(self) -> List[Type['Target']]:
        raise NotImplementedError("")


    def NAME(self) -> str:
        raise NotImplementedError("")

    def pythonanywhere_username(self) -> str:
        raise NotImplementedError("")

    def github_username(self) -> str:
        return self.sitedeployer().github_username()

    def github_url_type(self) -> str:
        raise NotImplementedError("")


    def PATHDIR_root_projectrepository(self) -> Path:
        return self.PATHDIR_root() / self.NAME()

    def PATHDIR_root_ins_project(self) -> Path:
        return self.PATHDIR_root_ins() / self.NAME()

    def PATHDIR_root_instemp_project(self) -> Path:
        return self.PATHDIR_root_instemp() / self.NAME()



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



    def clonebuildinstalltemp(self) -> None:
        logger.info('Clone/Build/Install "%project%" temp project...'.replace('%project%', self.NAME()))
        log_environment(logger=logger)

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))
        PATHDIR_root_projectrepository_ins = self.PATHDIR_root_projectrepository() / 'src/ins'

        if PATHDIR_root_projectrepository_ins.is_dir() and not self.PATHDIR_root_instemp_project().is_dir():
            shutil.copytree(
                PATHDIR_root_projectrepository_ins,
                self.PATHDIR_root_instemp_project()
            )

        os.environ['PATH'] = str(self.PATHDIR_root_instemp_project() / 'bin') + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
        os.environ['PYTHONPATH'] = str(self.PATHDIR_root_instemp_project() / 'lib') + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))

        log_environment(logger=logger)
        logger.info('Clone/Build/Install "%project%" temp project!'.replace('%project%', self.NAME()))



    def clonebuildinstall(self) -> None:
        logger.info('Clone/Build/Install "%project%" project...'.replace('%project%', self.NAME()))
        log_environment(logger=logger)

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.NAME()))
        PATHDIR_root_projectrepository_ins = self.PATHDIR_root_projectrepository() / 'src/ins'

        subprocess.run(
            ['projekt', 'task', 'build', 'default', 'execute'],
            cwd=self.PATHDIR_root_projectrepository(),
            # shell=True
        )

        if PATHDIR_root_projectrepository_ins.is_dir() and not self.PATHDIR_root_ins_project().is_dir():
            shutil.copytree(
                PATHDIR_root_projectrepository_ins,
                self.PATHDIR_root_ins_project()
            )

        os.environ['PATH'] = str(self.PATHDIR_root_ins_project() / 'bin') + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
        os.environ['PYTHONPATH'] = str(self.PATHDIR_root_ins_project() / 'lib') + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')

        if self.PATHDIR_root_instemp_project().is_dir():
            shutil.rmtree(self.PATHDIR_root_instemp_project())

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.NAME()))

        log_environment(logger=logger)
        logger.info('Clone/Build/Install "%project%" project!'.replace('%project%', self.NAME()))




    # projektorworkshop:
    def projektorworkshop_Type(self) -> str:
        raise NotImplementedError("")

    def projektorworkshop_projektorworkshopsitepubflaskpackage(self) -> str:
        return self.projektorworkshop_Type() + 'sitepub_' + self.NAME()

    def projektorworkshop_package(self) -> str:
        return self.projektorworkshop_Type() + '_' + self.NAME()
    
    def PATHDIR_root_projectrepository_projektorworkshop(self) -> Path:
        return self.PATHDIR_root_projectrepository() / ('_' + self.projektorworkshop_Type())


    def PATHDIR_root_projektorworkshop(self) -> Path:
        return self.PATHDIR_root() / ('_' + self.projektorworkshop_Type())

    def PATHDIR_root_projektorworkshop_projektorworkshoppackage(self) -> Path:
        return self.PATHDIR_root_projektorworkshop() / self.projektorworkshop_package()

    def PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage(self) -> Path:
        return self.PATHDIR_root_projektorworkshop() / self.projektorworkshop_projektorworkshopsitepubflaskpackage()


    def process_projektorworkshop(self) -> None:
        logger.info('Process projektorworkshop...')
        logger.info(
'''# projektorworkshop paths:
PATHDIR_root_projectrepository_projektorworkshop=%PATHDIR_root_projectrepository_projektorworkshop%

PATHDIR_root_projektorworkshop=%PATHDIR_root_projektorworkshop%
PATHDIR_root_projektorworkshop_projektorworkshoppackage=%PATHDIR_root_projektorworkshop_projektorworkshoppackage%
PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage=%PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage%'''

            .replace('%PATHDIR_root_projectrepository_projektorworkshop%', str(self.PATHDIR_root_projectrepository_projektorworkshop()))
            .replace('%PATHDIR_root_projektorworkshop%', str(self.PATHDIR_root_projektorworkshop()))
            .replace('%PATHDIR_root_projektorworkshop_projektorworkshoppackage%', str(self.PATHDIR_root_projektorworkshop_projektorworkshoppackage()))
            .replace('%PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage%', str(self.PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage()))
        )

        logger.info('Install projektorworkshop...')
        if self.PATHDIR_root_projectrepository().is_dir():
            shutil.copytree(
                self.PATHDIR_root_projectrepository_projektorworkshop(),
                self.PATHDIR_root_projektorworkshop()
            )
        logger.info('Install projektorworkshop!')
        logger.info('Process projektorworkshop!')
