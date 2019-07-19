import os, shutil, subprocess, sys
from pathlib import Path
import logging
from typing import Type, List

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Sitedeployer:
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy

    @staticmethod
    def target_Type() -> str:
        raise NotImplementedError("")

    @staticmethod
    def target_NAME() -> str:
        raise NotImplementedError("")


    @staticmethod
    def pythonanywhere_username() -> str:
        raise NotImplementedError("")


    @classmethod
    def sitepub_flask_package(cls) -> str:
        return cls.target_Type() + 'sitepub_' + cls.target_NAME()

    @classmethod
    def target_package(cls) -> str:
        return cls.target_Type() + '_' + cls.target_NAME()


    @classmethod
    def URL_site(cls) -> str:
        return cls.pythonanywhere_username() + '.pythonanywhere.com'

    @staticmethod
    def github_username() -> str:
        return 'ynsight'

    @staticmethod
    def github_url_type() -> str:
        raise NotImplementedError("")

    @staticmethod
    def ynsight_dependencies() -> List[Type['Sitedeployer']]:
        raise NotImplementedError("")









    # common:
    def PATHDIR_home_pythonanywhereusername_root(self) -> Path:
        return self._PATHFILE_deploypy.parent.parent.parent

    def PATHDIR_home_pythonanywhereusername(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root().parent

    def PATHDIR_root_third(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'third'

    def PATHDIR_root_repositories(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'repositories'

    def process_common(self) -> None:
        logger.info('[deployer] Process common...')

        logger.info('[deployer] Resolve common paths...')
        logger.info(
'''pythonanywhere_username=%pythonanywhere_username%
target_NAME=%target_NAME%
sitepub_flask_package=%sitepub_flask_package%
URL_site=%URL_site%

PATHDIR_home_pythonanywhereusername_root=%PATHDIR_home_pythonanywhereusername_root%
PATHDIR_home_pythonanywhereusername=%PATHDIR_home_pythonanywhereusername%

PATHDIR_root_third=%PATHDIR_root_third%
PATHDIR_root_repositories=%PATHDIR_root_repositories%'''
            .replace('%pythonanywhere_username%', str(self.pythonanywhere_username()))
            .replace('%target_NAME%', str(self.target_NAME()))
            .replace('%sitepub_flask_package%', str(self.sitepub_flask_package()))
            .replace('%URL_site%', str(self.URL_site()))
            \
            .replace('%PATHDIR_home_pythonanywhereusername_root%', str(self.PATHDIR_home_pythonanywhereusername_root()))
            .replace('%PATHDIR_home_pythonanywhereusername%', str(self.PATHDIR_home_pythonanywhereusername()))
            .replace('%PATHDIR_root_third%', str(self.PATHDIR_root_third()))
            .replace('%PATHDIR_root_repositories%', str(self.PATHDIR_root_repositories()))
        )
        logger.info('[deployer] Resolve common paths!')

        logger.info('[deployer] Make common dirs...')
        self.PATHDIR_root_repositories().mkdir(parents=True)
        self.PATHDIR_root_third().mkdir(parents=True)
        logger.info('[deployer] Make common dirs!')

        logger.info('[deployer] Process common!')






    # ynsight dependencies:
    def process_ynsight_dependency(self,
        ynsight_dependency:'Type[Sitedeployer]'=None
    ) -> None:
        logger.info('[deployer] Process ynsight dependency: "%ynsight_dependency%"...'.replace('%ynsight_dependency%', ynsight_dependency.target_NAME()))

        logger.info('[deployer] Resolve ynsight dependency...')
        ynsdep__target_NAME = ynsight_dependency.target_NAME()
        ynsdep__URL_github_target_repository = ynsight_dependency.URL_github_target_repository()
        ynsdep__PATHDIR_root_repositories_ynsdeprepository = self.PATHDIR_root_repositories() / ynsdep__target_NAME

        ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage = ynsdep__PATHDIR_root_repositories_ynsdeprepository / ('src/ins/lib/' + ynsdep__target_NAME)
        ynsdep__PATHDIR_root_third_ynsdeppackage = self.PATHDIR_root_third() / ynsdep__target_NAME

        logger.info(
'''ynsdep__target_NAME=%ynsdep__target_NAME%
ynsdep__URL_github_target_repository=%ynsdep__URL_github_target_repository%
ynsdep__PATHDIR_root_repositories_ynsdeprepository=%ynsdep__PATHDIR_root_repositories_ynsdeprepository%

ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage=%ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage%
ynsdep__PATHDIR_root_third_ynsdeppackage=%ynsdep__PATHDIR_root_third_ynsdeppackage%'''
            .replace('%ynsdep__target_NAME%', ynsdep__target_NAME)
            .replace('%ynsdep__URL_github_target_repository%', ynsdep__URL_github_target_repository)
            .replace('%ynsdep__PATHDIR_root_repositories_ynsdeprepository%', str(ynsdep__PATHDIR_root_repositories_ynsdeprepository))

            .replace('%ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage%', str(ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage))
            .replace('%ynsdep__PATHDIR_root_third_ynsdeppackage%', str(ynsdep__PATHDIR_root_third_ynsdeppackage))
        )
        logger.info('[deployer] Resolve ynsight dependency!')

        logger.info('[deployer] Install ynsight dependency...')
        subprocess.run(
            ['git', 'clone', ynsdep__URL_github_target_repository],
            cwd=str(self.PATHDIR_root_repositories())
        )

        if ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage.is_dir():
            shutil.copytree(
                ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage,
                ynsdep__PATHDIR_root_third_ynsdeppackage
            )
        logger.info('[deployer] Install ynsight dependency!')

        logger.info('[deployer] Process ynsight dependency: "%ynsight_dependency%"!'.replace('%ynsight_dependency%', ynsight_dependency.target_NAME()))

    def process_ynsight_dependencies(self) -> None:
        logger.info('[deployer] Process ynsight dependencies...')

        for ynsight_dependency in self.ynsight_dependencies():
            self.process_ynsight_dependency(
                ynsight_dependency=ynsight_dependency
            )

        logger.info('[deployer] Process ynsight dependencies!')


    # sitedeployer:
    def PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy(self) -> Path:
        return self._PATHFILE_deploypy

    def PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage(self) -> Path:
        return self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy().parent

    def PATHDIR_home_pythonanywhereusername_root_sitedeployer(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage().parent

    def process_sitedeployer(self) -> None:
        logger.info('[deployer] Process sitedeployer...')

        logger.info('[deployer] Resolve sitedeployer paths...')

        logger.info(
'''PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy=%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy%
PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage=%PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage%
PATHDIR_home_pythonanywhereusername_root_sitedeployer=%PATHDIR_home_pythonanywhereusername_root_sitedeployer%'''
                .replace('%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy%',
                         str(self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy()))
                .replace('%PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage%',
                         str(self.PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage()))
                .replace('%PATHDIR_home_pythonanywhereusername_root_sitedeployer%', str(self.PATHDIR_home_pythonanywhereusername_root_sitedeployer()))
        )

        logger.info('[deployer] Resolve sitedeployer paths!')

        logger.info('[deployer] Process sitedeployer!')



    # target:
    def PATHDIR_root_repositories_targetrepository(self) -> Path:
        return self.PATHDIR_root_repositories() / self.target_NAME()

    @classmethod
    def URLSSH_github_target_repository(cls) -> str:
        return '''git@github.com:%github_username%/%target_NAME%.git'''\
            .replace('%target_NAME%', cls.target_NAME())\
            .replace('%github_username%', cls.github_username())

    @classmethod
    def URLHTTP_github_target_repository(cls) -> str:
        return '''http://github.com/%github_username%/%target_NAME%.git'''\
            .replace('%target_NAME%', cls.target_NAME())\
            .replace('%github_username%', cls.github_username())

    @classmethod
    def URLHTTPS_github_target_repository(cls) -> str:
        return '''https://github.com/%github_username%/%target_NAME%.git'''\
            .replace('%target_NAME%', cls.target_NAME())\
            .replace('%github_username%', cls.github_username())

    @classmethod
    def URL_github_target_repository(cls) -> str:
        result = None
        if   cls.github_url_type() == 'ssh':
            result = cls.URLSSH_github_target_repository()
        elif cls.github_url_type() == 'http':
            result = cls.URLHTTP_github_target_repository()
        elif cls.github_url_type() == 'https':
            result = cls.URLHTTPS_github_target_repository()
        return result


    def process_target_repository(self) -> None:
        logger.info('[deployer] Process target repository...')
        logger.info(
'''project paths:
target_NAME=%target_NAME%

github_url_type=%github_url_type%

URLSSH_github_target_repository=%URLSSH_github_target_repository%
URLHTTP_github_target_repository=%URLHTTP_github_target_repository%
URLHTTPS_github_target_repository=%URLHTTPS_github_target_repository%

URL_github_target_repository=%URLSSH_github_target_repository%

PATHDIR_root_repositories_targetrepository=%PATHDIR_root_repositories_targetrepository%'''
            .replace('%target_NAME%', str(self.target_NAME()))

            .replace('%github_url_type%', str(self.github_url_type()))

            .replace('%URLSSH_github_target_repository%', str(self.URLSSH_github_target_repository()))
            .replace('%URLHTTP_github_target_repository%', str(self.URLHTTP_github_target_repository()))
            .replace('%URLHTTPS_github_target_repository%', str(self.URLHTTPS_github_target_repository()))

            .replace('%URLSSH_github_target_repository%', str(self.URLSSH_github_target_repository()))

            .replace('%PATHDIR_root_repositories_targetrepository%', str(self.PATHDIR_root_repositories_targetrepository()))
        )

        logger.info('[deployer] Cloning target repository...')
        subprocess.run(
            ['git', 'clone', self.URLSSH_github_target_repository()],
            cwd=str(self.PATHDIR_root_repositories())
        )
        logger.info('[deployer] Cloning target repository!')
        logger.info('[deployer] Process target repository!')



    # target:
    def PATHDIR_root_repositories_targetrepository_target(self) -> Path:
        return self.PATHDIR_root_repositories_targetrepository() / ('_' + self.target_Type())


    def PATHDIR_root_target(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / ('_' + self.target_Type())

    def PATHDIR_root_target_targetpackage(self) -> Path:
        return self.PATHDIR_root_target() / self.target_package()

    def PATHDIR_root_target_sitepubflaskpackage(self) -> Path:
        return self.PATHDIR_root_target() / self.sitepub_flask_package()


    def process_target(self) -> None:
        logger.info('[deployer] Process target...')
        logger.info(
'''# target paths:
PATHDIR_root_repositories_targetrepository_target=%PATHDIR_root_repositories_targetrepository_target%

PATHDIR_root_target=%PATHDIR_root_target%
PATHDIR_root_target_targetpackage=%PATHDIR_root_target_targetpackage%
PATHDIR_root_target_sitepubflaskpackage=%PATHDIR_root_target_sitepubflaskpackage%'''

            .replace('%PATHDIR_root_repositories_targetrepository_target%', str(self.PATHDIR_root_repositories_targetrepository_target()))
            .replace('%PATHDIR_root_target%', str(self.PATHDIR_root_target()))
            .replace('%PATHDIR_root_target_targetpackage%', str(self.PATHDIR_root_target_targetpackage()))
            .replace('%PATHDIR_root_target_sitepubflaskpackage%', str(self.PATHDIR_root_target_sitepubflaskpackage()))
        )


        logger.info('[deployer] Install target...')
        if self.PATHDIR_root_repositories_targetrepository().is_dir():
            shutil.copytree(
                self.PATHDIR_root_repositories_targetrepository_target(),
                self.PATHDIR_root_target()
            )
        logger.info('[deployer] Install target!')
        logger.info('[deployer] Process target!')



    # wsgi.py:
    def PATHFILE_wsgipy(self) -> Path:
        return Path(
                '/var/www/%pythonanywhere_username%_pythonanywhere_com_wsgi.py'
                    .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            )

    def process_wsgipy(self) -> None:
        logger.info('[deployer] Process wsgi.py...')

        logger.info(
'''wsgi.py paths:
PATHFILE_wsgipy=%PATHFILE_wsgipy%'''
            .replace('%PATHFILE_wsgipy%', str(self.PATHFILE_wsgipy()))
        )

        logger.info('[deployer] Write wsgi.py file...')
        wsgipy_template = \
'''import sys

target_home = u'/home/%pythonanywhere_username%/root/_%target%'
if not target_home in sys.path:
    sys.path = [target_home] + sys.path

sys.path = ['/home/%pythonanywhere_username%/root/third'] + sys.path

from %sitepub_flask_package%.flask_app import app as application
'''

        self.PATHFILE_wsgipy().write_text(
            wsgipy_template
                .replace('%pythonanywhere_username%', self.pythonanywhere_username())
                .replace('%sitepub_flask_package%', self.sitepub_flask_package())
                .replace('%target%', self.target_Type())
        )
        logger.info('[deployer] Write wsgi.py file!')

        logger.info('[deployer] Process wsgi.py!')



    # update.py:
    def PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage() / 'update.py'

    def PATHFILE_home_pythonanywhereusername_updatepy(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername() / 'update.py'

    def process_updatepy(self) -> None:
        logger.info('[deployer] Process update.py...')

        logger.info(
'''update.py paths:
PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy=%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy%
PATHFILE_home_pythonanywhereusername_updatepy=%PATHFILE_home_pythonanywhereusername_updatepy%'''
            .replace('%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy()))
            .replace('%PATHFILE_home_pythonanywhereusername_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_updatepy()))
        )

        logger.info('[deployer] Write update.py file...')
        shutil.copyfile(
            self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy(),
            self.PATHFILE_home_pythonanywhereusername_updatepy()
        )
        logger.info('[deployer] Write update.py file!')

        logger.info('[deployer] Process update.py!')


    def Execute(self) -> None:
        self.process_common()
        self.process_sitedeployer()
        self.process_ynsight_dependencies()
        self.process_target_repository()
        self.process_target()
        self.process_wsgipy()
        self.process_updatepy()