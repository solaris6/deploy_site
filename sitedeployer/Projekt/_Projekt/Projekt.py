import os
import shutil

import subprocess
from pathlib import Path
from typing import Type, List

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[sitedeployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

class Projekt:
    def __init__(self):
        self._sitedeployer = None

    def attach_to_sitedeployer(self,
        sitedeployer:'Sitedeployer'=None
    ) -> None:
        logger.info(
            'Attaching "%NAME%" project to sitedeployer...'
                .replace('%NAME%', self.NAME())
        )
        if not self._sitedeployer is None:
            logger.info(
                'Project "%NAME%" already attached to sitedeployer, skipping...'
                    .replace('%NAME%', self.NAME())
            )
        else:
            self._sitedeployer = sitedeployer
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
            )

            logger.info('Init Projekt!')
            logger.info(
                'Attached "%NAME%" project to sitedeployer!'
                    .replace('%NAME%', self.NAME())
            )

    def sitedeployer(self) -> 'Sitedeployer':
        return self._sitedeployer

    # names:
    def NAME(self) -> str:
        raise NotImplementedError("")

    def version_list(self) -> List[int]:
        raise NotImplementedError("")

    def version_dot_str(self) -> str:
        return '.'.join(self.version_list())

    def DIRNAME_egg(self) -> str:
        return '%NAME%-%project_version_dot_str%-py%python_version_dot_str%.egg'\
            .replace('%NAME%', self.NAME())\
            .replace('%project_version_dot_str%', self.sitedeployer().version_dot_str())\
            .replace('%python_version_dot_str%', self.sitedeployer().python_version_dot_str())

    def PATHDIR_egg(self) -> Path:
        return self.sitedeployer().PATHDIR_venvsitepackages() / self.DIRNAME_egg()


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

    def PATHDIRS_packages_to_upload_on_pypi(self) -> List[Path]:
        return []

    def upload_on_pypi(self) -> None:
        PATHDIR_testpy = self.sitedeployer().PATHDIR_root() / 'pypi'
        if PATHDIR_testpy.is_dir():
            shutil.rmtree()
        PATHDIR_testpy.mkdir(parents=True)

        PATHDIR_testpy_projektrepository = PATHDIR_testpy / self.NAME()

        subprocess.run(
            ['git', 'clone', self.URL_github_projekt_repository()],
            cwd=str(PATHDIR_testpy)
        )

        os.environ['TWINE_USERNAME'] = '__token__'
        PATHFILE_YNSIGHT_PYPI_TOKEN_txt = self.sitedeployer().PATHDIR_home_pythonanywhereusername() / 'YNSIGHT_TESTPYPI_TOKEN.txt'
        if PATHFILE_YNSIGHT_PYPI_TOKEN_txt.is_file():
            YNSIGHT_PYPI_TOKEN = PATHFILE_YNSIGHT_PYPI_TOKEN_txt.read_text()
        else:
            YNSIGHT_PYPI_TOKEN = ''
        os.environ['TWINE_PASSWORD'] = YNSIGHT_PYPI_TOKEN

        subprocess.run(
            ['python3', 'upload.py'],
            cwd=str(PATHDIR_testpy_projektrepository)
        )

    # pythonanywhere:
    def pythonanywhere_username(self) -> str:
        raise NotImplementedError("")

    def wsgipy_entry(self) -> str:
        return \
'''sys.path = ['%PATHDIR_root_out_projekt%'] + sys.path'''\
            .replace('%PATHDIR_root_out_projekt%', str(self.PATHDIR_root_out_projekt()))

    def uninstall_as_package(self) -> None:
        logger.info('Unnstall as as package "%projekt%"...'.replace('%projekt%', self.NAME()))
        if self.is_uninstall_as_package_supported():
            PATHDIR_venvsitepackages = self.sitedeployer().PATHDIR_venvsitepackages()

            logger.info('Remove "%projekt%" package...'.replace('%projekt%', self.NAME()))
            prev_installation_exists = False
            if PATHDIR_venvsitepackages.is_dir():
                for item in os.listdir(PATHDIR_venvsitepackages):
                    PATHDIR_egg = PATHDIR_venvsitepackages / item
                    if item.startswith(self.NAME()) and\
                       item.endswith('-py%python_version_dot_str%.egg'.replace('%python_version_dot_str%', self.sitedeployer().python_version_dot_str())) and\
                            PATHDIR_egg.is_dir():
                        logger.info('Previous installation exists, deleting("' + str(PATHDIR_egg) + '")...')
                        shutil.rmtree(PATHDIR_egg)
                        prev_installation_exists = True
                    else:
                        logger.info('Item is NOT previous installation, skipping("' + str(PATHDIR_egg) + '")...')

            logger.info('Removed "%projekt%" package!'.replace('%projekt%', self.NAME()))

            logger.info('Remove "%projekt%" executables...'.replace('%projekt%', self.NAME()))
            for package_executable in self.package_executables():
                PATHFILE_package_executable = self.sitedeployer().PATHDIR_venvbin() / package_executable

                if PATHFILE_package_executable.is_file():
                    logger.info('Executable exists, deleting("' + str(PATHFILE_package_executable) + '")...')
                    os.remove(str(PATHFILE_package_executable))
                    prev_installation_exists = True
                else:
                    logger.info('Executable NOT exists, skipping("' + str(PATHFILE_package_executable) + '")...')

            if not prev_installation_exists:
                logger.info('Previous installation NOT exists, skipping')
            logger.info('Uninstall as package "%projekt%"!'.replace('%projekt%', self.NAME()))
        else:
            logger.info('Uninstall as package "%projekt%" is NOT supported!'.replace('%projekt%', self.NAME()))

    def is_uninstall_as_package_supported(self) -> bool:
        raise NotImplementedError("")

    def package_executables(self) -> List[str]:
        raise NotImplementedError("")
