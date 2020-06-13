import os
import shutil

import subprocess
from pathlib import Path
from typing import Type, List

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[task] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

class Gitproject:
    def __init__(self):
        self._task = None

    def attach_to_task(self,
        task:'Sitetask'=None
    ) -> None:
        logger.info(
            'Attaching "%NAME%" project to task...'
                .replace('%NAME%', self.NAME())
        )
        if not self._task is None:
            logger.info(
                'Project "%NAME%" already attached to task, skipping...'
                    .replace('%NAME%', self.NAME())
            )
        else:
            self._task = task
            logger.info('Init Projekt...')
            logger.info(
'''# names:
NAME: '%NAME%'
projekt_package: '%projekt_package%'
projekt: '%project_or_workshop%'

# PATHS:
PATHDIR_root: '%PATHDIR_root%'
PATHDIR_root_projektrepository: '%PATHDIR_root_projektrepository%'

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
                .replace('%projekt_package%', self.projekt_package())
                .replace('%project_or_workshop%', self.project_or_workshop())
                \
                .replace('%PATHDIR_root%', str(self.PATHDIR_root()))
                .replace('%PATHDIR_root_projektrepository%', str(self.PATHDIR_root_projektrepository()))
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
                'Attached "%NAME%" project to task!'
                    .replace('%NAME%', self.NAME())
            )

    def task(self) -> 'Sitetask':
        return self._task

    # names:
    def NAME(self) -> str:
        raise NotImplementedError("")

    def version_list(self) -> List[int]:
        raise NotImplementedError("")


    def projektsitepub_package(self) -> str:
        return

    def projekt_package(self) -> str:
        return '%project_or_workshop%_%NAME%'\
            .replace('%project_or_workshop%', self.project_or_workshop())\
            .replace('%NAME%', self.NAME())

    def project_or_workshop(self) -> str:

        if self.NAME() == 'ynsight':
            result = 'workshop'
        else:
            result = 'project'
        return result

    # PATHS:
    def PATHDIR_root(self) -> Path:
        return self.task().PATHDIR_root()

    def PATHDIR_root_projektrepository(self) -> Path:
        return self.PATHDIR_root() / self.NAME()


    # github:
    def github_username(self) -> str:
        return self.task().github_username()

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

    def upload_on_pypi(self) -> None:
        PATHDIR_testpy = self.task().PATHDIR_root() / 'pypi'
        if PATHDIR_testpy.is_dir():
            shutil.rmtree(
                PATHDIR_testpy,
                ignore_errors=True
            )
        PATHDIR_testpy.mkdir(
            parents=True
        )

        PATHDIR_testpy_projektrepository = PATHDIR_testpy / self.NAME()

        subprocess.run(
            [
                'git',
                'clone',
                self.URL_github_projekt_repository()
            ],
            cwd=str(PATHDIR_testpy)
        )

        PATHFILE_YNSIGHT_PYPI_PWD_txt = Path(self.task().PATHDIR_home_pythonanywhereusername(), 'YNSIGHT_PYPI_PWD.txt')
        if PATHFILE_YNSIGHT_PYPI_PWD_txt.is_file():
            os.environ['TWINE_USERNAME'] = 'ynsight'
            os.environ['TWINE_PASSWORD'] = PATHFILE_YNSIGHT_PYPI_PWD_txt.read_text()
            subprocess.run(
                [
                    'python3',
                    'upload.py'
                ],
                cwd=str(PATHDIR_testpy_projektrepository)
            )
        else:
            logger.error('PATHFILE_YNSIGHT_PYPI_PWD_txt NOT exists at "%PATHFILE%", upload canceled...'.replace('%PATHFILE%', PATHFILE_YNSIGHT_PYPI_PWD_txt))


    # pythonanywhere:
    def pythonanywhere_username(self) -> str:
        raise NotImplementedError("")

    def uninstall_as_package(self) -> None:
        logger.info('Unnstall as package "%projekt%"...'.replace('%projekt%', self.NAME()))
        if self.is_uninstall_as_package_supported():
            PATHDIR_venvsitepackages = self.task().PATHDIR_venvsitepackages()

            logger.info('Remove "%projekt%" package...'.replace('%projekt%', self.NAME()))
            prev_installation_exists = False
            if PATHDIR_venvsitepackages.is_dir():
                for item in os.listdir(PATHDIR_venvsitepackages):
                    PATHDIR_item = PATHDIR_venvsitepackages / item

                    if PATHDIR_item.is_dir():
                        if item == self.NAME() or item.startswith(self.NAME() + '-'):
                            logger.info('Previous installation exists, deleting("' + str(PATHDIR_item) + '")...')
                            shutil.rmtree(
                                PATHDIR_item,
                                ignore_errors=True
                            )
                            prev_installation_exists = True
                        else:
                            logger.info('Item is NOT previous installation, skipping("' + str(PATHDIR_item) + '")...')

            logger.info('Removed "%projekt%" package!'.replace('%projekt%', self.NAME()))

            logger.info('Remove "%projekt%" executables...'.replace('%projekt%', self.NAME()))
            for package_executable in self.package_executables():
                PATHFILE_package_executable = self.task().PATHDIR_venvbin() / package_executable

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
