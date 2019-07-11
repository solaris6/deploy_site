import os, shutil, subprocess, sys
from pathlib import Path
import logging
from typing import Type, List

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.info('deploy.py imported')

class Sitedeployer:
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy

    @staticmethod
    def project_NAME() -> str:
        raise NotImplementedError("")

    @staticmethod
    def pythonanywhere_username() -> str:
        raise NotImplementedError("")

    @classmethod
    def site_flask_package(cls) -> str:
        return 'site_' + cls.project_NAME()

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
        return self._PATHFILE_deploypy.parent.parent

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
project_NAME=%project_NAME%

PATHDIR_home_pythonanywhereusername_root=%PATHDIR_home_pythonanywhereusername_root%
PATHDIR_home_pythonanywhereusername=%PATHDIR_home_pythonanywhereusername%

PATHDIR_root_third=%PATHDIR_root_third%
PATHDIR_root_repositories=%PATHDIR_root_repositories%'''
            .replace('%pythonanywhere_username%', str(self.pythonanywhere_username()))
            .replace('%project_NAME%', str(self.project_NAME()))
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
        logger.info('[deployer] Process ynsight dependency: "%ynsight_dependency%"...'.replace('%ynsight_dependency%', ynsight_dependency.project_NAME()))

        logger.info('[deployer] Resolve ynsight dependency...')
        ynsdep__project_NAME = ynsight_dependency.project_NAME()
        ynsdep__URL_github_project_repository = ynsight_dependency.URL_github_project_repository()
        ynsdep__PATHDIR_root_repositories_ynsdeprepository = self.PATHDIR_root_repositories() / ynsdep__project_NAME

        ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage = ynsdep__PATHDIR_root_repositories_ynsdeprepository / ('src/ins/lib/' + ynsdep__project_NAME)
        ynsdep__PATHDIR_root_third_ynsdeppackage = self.PATHDIR_root_third() / ynsdep__project_NAME

        logger.info(
'''ynsdep__project_NAME=%ynsdep__project_NAME%
ynsdep__URL_github_project_repository=%ynsdep__URL_github_project_repository%
ynsdep__PATHDIR_root_repositories_ynsdeprepository=%ynsdep__PATHDIR_root_repositories_ynsdeprepository%

ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage=%ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage%
ynsdep__PATHDIR_root_third_ynsdeppackage=%ynsdep__PATHDIR_root_third_ynsdeppackage%'''
            .replace('%ynsdep__project_NAME%', ynsdep__project_NAME)
            .replace('%ynsdep__URL_github_project_repository%', ynsdep__URL_github_project_repository)
            .replace('%ynsdep__PATHDIR_root_repositories_ynsdeprepository%', str(ynsdep__PATHDIR_root_repositories_ynsdeprepository))

        )
        logger.info('[deployer] Resolve ynsight dependency!')

        logger.info('[deployer] Install ynsight dependency...')
        subprocess.run(
            ['git', 'clone', ynsdep__URL_github_project_repository],
            cwd=str(self.PATHDIR_root_repositories())
        )

        if ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage.is_dir():
            shutil.copytree(
                ynsdep__PATHDIR_root_repositories_ynsdeprepository_ynsdeppackage,
                ynsdep__PATHDIR_root_third_ynsdeppackage
            )
        logger.info('[deployer] Install ynsight dependency!')

        logger.info('[deployer] Process ynsight dependency: "%ynsight_dependency%"!'.replace('%ynsight_dependency%', ynsight_dependency.project_NAME()))

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



    # project:
    def PATHDIR_root_repositories_projectrepository(self) -> Path:
        return self.PATHDIR_root_repositories() / self.project_NAME()

    @classmethod
    def URLSSH_github_project_repository(cls) -> str:
        return '''git@github.com:%github_username%/%project_NAME%.git'''\
            .replace('%project_NAME%', cls.project_NAME())\
            .replace('%github_username%', cls.github_username())

    @classmethod
    def URLHTTP_github_project_repository(cls) -> str:
        return '''http://github.com/%github_username%/%project_NAME%.git'''\
            .replace('%project_NAME%', cls.project_NAME())\
            .replace('%github_username%', cls.github_username())

    @classmethod
    def URLHTTPS_github_project_repository(cls) -> str:
        return '''https://github.com/%github_username%/%project_NAME%.git'''\
            .replace('%project_NAME%', cls.project_NAME())\
            .replace('%github_username%', cls.github_username())

    @classmethod
    def URL_github_project_repository(cls) -> str:
        result = None
        if   cls.github_url_type() == 'ssh':
            result = cls.URLSSH_github_project_repository()
        elif cls.github_url_type() == 'http':
            result = cls.URLHTTP_github_project_repository()
        elif cls.github_url_type() == 'https':
            result = cls.URLHTTPS_github_project_repository()
        return result


    def process_project(self) -> None:
        logger.info('[deployer] Process project...')

        logger.info(
'''project paths:
project_NAME=%project_NAME%

github_url_type=%github_url_type%

URLSSH_github_project_repository=%URLSSH_github_project_repository%
URLHTTP_github_project_repository=%URLHTTP_github_project_repository%
URLHTTPS_github_project_repository=%URLHTTPS_github_project_repository%

URL_github_project_repository=%URLSSH_github_project_repository%

PATHDIR_root_repositories_projectrepository=%PATHDIR_root_repositories_projectrepository%'''
            .replace('%project_NAME%', str(self.project_NAME()))

            .replace('%github_url_type%', str(self.github_url_type()))

            .replace('%URLSSH_github_project_repository%', str(self.URLSSH_github_project_repository()))
            .replace('%URLHTTP_github_project_repository%', str(self.URLHTTP_github_project_repository()))
            .replace('%URLHTTPS_github_project_repository%', str(self.URLHTTPS_github_project_repository()))

            .replace('%URLSSH_github_project_repository%', str(self.URLSSH_github_project_repository()))

            .replace('%PATHDIR_root_repositories_projectrepository%', str(self.PATHDIR_root_repositories_projectrepository()))
        )


        logger.info('[deployer] Downloading project repository...')
        subprocess.run(
            ['git', 'clone', self.URLSSH_github_project_repository()],
            cwd=str(self.PATHDIR_root_repositories())
        )
        logger.info('[deployer] Downloading project repository!')

        logger.info('[deployer] Process project!')



    # site:
    def PATHDIR_root_site(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'site'

    def PATHDIR_root_site_lib(self) -> Path:
        return self.PATHDIR_root_site() / 'lib'

    def PATHDIR_root_site_lib_siteflaskpackage(self) -> Path:
        return self.PATHDIR_root_site_lib() / self.site_flask_package()

    def PATHDIR_root_repositories_projectrepository_site(self) -> Path:
        return self.PATHDIR_root_repositories_projectrepository() / 'src/site'

    def process_site(self) -> None:
        logger.info('[deployer] Process site...')

        logger.info(
'''site paths:
site_flask_package=%site_flask_package%
URL_site=%URL_site%
PATHDIR_root_site=%PATHDIR_root_site%
PATHDIR_root_site_lib=%PATHDIR_root_site_lib%
PATHDIR_root_site_lib_siteflaskpackage=%PATHDIR_root_site_lib_siteflaskpackage%

PATHDIR_root_repositories_projectrepository_site=%PATHDIR_root_repositories_projectrepository_site%'''
            .replace('%site_flask_package%', str(self.site_flask_package()))
            .replace('%URL_site%', str(self.URL_site()))
            .replace('%URLSSH_github_project_repository%', str(self.URLSSH_github_project_repository()))
\
            .replace('%PATHDIR_root_site%', str(self.PATHDIR_root_site()))
            .replace('%PATHDIR_root_site_lib%', str(self.PATHDIR_root_site_lib()))
            .replace('%PATHDIR_root_site_lib_siteflaskpackage%', str(self.PATHDIR_root_site_lib_siteflaskpackage()))
            .replace('%PATHDIR_root_repositories_projectrepository_site%', str(self.PATHDIR_root_repositories_projectrepository_site()))
        )

        logger.info('[deployer] Install project site...')
        if self.PATHDIR_root_repositories_projectrepository().is_dir():
            shutil.copytree(
                self.PATHDIR_root_repositories_projectrepository_site(),
                self.PATHDIR_root_site()
            )
        logger.info('[deployer] Install project site!')

        logger.info('[deployer] Process site!')



    # doc:
    def docpackage(self) -> str:
        return 'doc_' + self.project_NAME()

    def PATHDIR_root_doc(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'doc'

    def PATHDIR_root_doc_lib(self) -> Path:
        return self.PATHDIR_root_doc() / 'lib'

    def PATHDIR_root_doc_lib_docpackage(self) -> Path:
        return self.PATHDIR_root_doc_lib() / self.docpackage()

    def PATHDIR_root_repositories_projectrepository_doc(self) -> Path:
        return self.PATHDIR_root_repositories_projectrepository() / 'src/doc'

    def process_doc(self) -> None:
        logger.info('[deployer] Process doc...')

        logger.info(
'''doc paths:
docpackage=%docpackage%
PATHDIR_root_doc=%PATHDIR_root_doc%
PATHDIR_root_doc_lib=%PATHDIR_root_doc_lib%
PATHDIR_root_doc_lib_docpackage=%PATHDIR_root_doc_lib_docpackage%
PATHDIR_root_repositories_projectrepository_doc=%PATHDIR_root_repositories_projectrepository_doc%'''
            .replace('%docpackage%', str(self.docpackage()))
            .replace('%PATHDIR_root_doc%', str(self.PATHDIR_root_doc()))
            .replace('%PATHDIR_root_doc_lib%', str(self.PATHDIR_root_doc_lib()))
            .replace('%PATHDIR_root_doc_lib_docpackage%', str(self.PATHDIR_root_doc_lib_docpackage()))
            .replace('%PATHDIR_root_repositories_projectrepository_doc%', str(self.PATHDIR_root_repositories_projectrepository_doc()))
        )

        logger.info('[deployer] Install project doc...')
        if self.PATHDIR_root_repositories_projectrepository().is_dir():
            shutil.copytree(
                self.PATHDIR_root_repositories_projectrepository_doc(),
                self.PATHDIR_root_doc()
            )
        logger.info('[deployer] Install project doc!')

        logger.info('[deployer] Process doc!')



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

project_home = u'/home/%pythonanywhere_username%/root/site/lib'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

sys.path = ['/home/%pythonanywhere_username%/root/doc/lib'] + sys.path
sys.path = ['/home/%pythonanywhere_username%/root/third'] + sys.path

from %site_flask_package%.main import app as application
'''

        self.PATHFILE_wsgipy().write_text(
            wsgipy_template
                .replace('%pythonanywhere_username%', self.pythonanywhere_username())
                .replace('%site_flask_package%', self.site_flask_package())
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
        self.process_project()
        self.process_site()
        self.process_doc()
        self.process_wsgipy()
        self.process_updatepy()



# base:
class base_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'base'
    
    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getbase'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies() -> List[Type[Sitedeployer]]:
        return [
            base_Sitedeployer,
            project_Sitedeployer,
            myrta_Sitedeployer,
            # una_Sitedeployer,
            # rs_Sitedeployer,
            # fw_Sitedeployer,
            # sola_Sitedeployer,
            # Ln_Sitedeployer,
            # ynsight_Sitedeployer
        ]



# project:
class project_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'project'

    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getprojekt'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies() -> List[Type[Sitedeployer]]:
        return [
            base_Sitedeployer,
            project_Sitedeployer,
            myrta_Sitedeployer,
            # una_Sitedeployer,
            # rs_Sitedeployer,
            # fw_Sitedeployer,
            # sola_Sitedeployer,
            # Ln_Sitedeployer,
            # ynsight_Sitedeployer
        ]



# myrta:
class myrta_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'myrta'
    
    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getmyrta'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies() -> List[Type[Sitedeployer]]:
        return [
            base_Sitedeployer,
            project_Sitedeployer,
            myrta_Sitedeployer,
            # una_Sitedeployer,
            # rs_Sitedeployer,
            # fw_Sitedeployer,
            # sola_Sitedeployer,
            # Ln_Sitedeployer,
            # ynsight_Sitedeployer
        ]



# una:
class una_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'una'
    
    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getuna'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies() -> List[Type[Sitedeployer]]:
        return [
            base_Sitedeployer,
            project_Sitedeployer,
            myrta_Sitedeployer,
            # una_Sitedeployer,
            # rs_Sitedeployer,
            # fw_Sitedeployer,
            # sola_Sitedeployer,
            # Ln_Sitedeployer,
            # ynsight_Sitedeployer
        ]



# rs:
class rs_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'rs'
    
    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getrs'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies() -> List[Type[Sitedeployer]]:
        return [
            base_Sitedeployer,
            project_Sitedeployer,
            myrta_Sitedeployer,
            una_Sitedeployer,
            # rs_Sitedeployer,
            # fw_Sitedeployer,
            # sola_Sitedeployer,
            # Ln_Sitedeployer,
            # ynsight_Sitedeployer
        ]



# fw:
class fw_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'fw'
    
    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getfw'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies() -> List[Type[Sitedeployer]]:
        return [
            base_Sitedeployer,
            project_Sitedeployer,
            myrta_Sitedeployer,
            una_Sitedeployer,
            # rs_Sitedeployer,
            # fw_Sitedeployer,
            # sola_Sitedeployer,
            # Ln_Sitedeployer,
            # ynsight_Sitedeployer
        ]



# sola:
class sola_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'sola'

    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getsola'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies() -> List[Type[Sitedeployer]]:
        return [
            base_Sitedeployer,
            project_Sitedeployer,
            myrta_Sitedeployer,
            una_Sitedeployer,
            # rs_Sitedeployer,
            # fw_Sitedeployer,
            # sola_Sitedeployer,
            # Ln_Sitedeployer,
            # ynsight_Sitedeployer
        ]



# Ln:
class Ln_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'Ln'
    
    @staticmethod
    def pythonanywhere_username() -> str:
        return 'getln'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies() -> List[Type[Sitedeployer]]:
        return [
            base_Sitedeployer,
            project_Sitedeployer,
            myrta_Sitedeployer,
            una_Sitedeployer,
            # rs_Sitedeployer,
            fw_Sitedeployer,
            # sola_Sitedeployer,
            # Ln_Sitedeployer,
            # ynsight_Sitedeployer
        ]



# ynsight:
class ynsight_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    @staticmethod
    def project_NAME() -> str:
        return 'ynsight'
    
    @staticmethod
    def pythonanywhere_username() -> str:
        return 'ynsight'

    @staticmethod
    def github_url_type() -> str:
        return 'ssh'

    @staticmethod
    def ynsight_dependencies() -> List[Type[Sitedeployer]]:
        return [
            base_Sitedeployer,
            project_Sitedeployer,
            myrta_Sitedeployer,
            una_Sitedeployer,
            rs_Sitedeployer,
            fw_Sitedeployer,
            # sola_Sitedeployer,
            # Ln_Sitedeployer,
            # ynsight_Sitedeployer
        ]

    def process_doc(self) -> None:
        pass


def Sitedeployer__from__PATHFILE_deploypy(
    PATHFILE_deploypy:Path=None
) -> Sitedeployer:
    pythonanywhere_username = PATHFILE_deploypy.parent.parent.parent.parent.name
    return {
        'getbase': base_Sitedeployer,
        'getprojekt': project_Sitedeployer,
        'getmyrta': myrta_Sitedeployer,
        'getuna': una_Sitedeployer,
        'getrs': rs_Sitedeployer,
        'getfw': fw_Sitedeployer,
        'getsola': sola_Sitedeployer,
        'getln': Ln_Sitedeployer,
        'ynsight': ynsight_Sitedeployer
    }[pythonanywhere_username](
        PATHFILE_deploypy=PATHFILE_deploypy
    )



if __name__ == '__main__':
    logger.info('[deployer] Deploy site...')

    Sitedeployer__from__PATHFILE_deploypy(
        PATHFILE_deploypy=Path(sys.argv[0])
    ).Execute()

    logger.info('[deployer] Deploy site!')
