import os, shutil, subprocess, sys
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.info('deploy.py imported')

class Sitedeployer:
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy

    def project_NAME(self) -> str:
        raise NotImplementedError("")

    def USER(self) -> str:
        raise NotImplementedError("")

    def sitepackage(self) -> str:
        return 'site_' + self.project_NAME()

    def URL_site(self) -> str:
        return self.USER() + '.pythonanywhere.com'



    # common:
    def PATHDIR_home_user_root(self) -> Path:
        return self._PATHFILE_deploypy.parent.parent

    def PATHDIR_home_user(self) -> Path:
        return self.PATHDIR_home_user_root().parent

    def PATHDIR_root_third(self) -> Path:
        return self.PATHDIR_home_user_root() / 'third'

    def PATHDIR_root_repositories(self) -> Path:
        return self.PATHDIR_home_user_root() / 'repositories'

    def process_common(self) -> None:
        logger.info('[deployer] Process common...')

        logger.info('[deployer] Resolve common paths...')
        logger.info(
'''USER=%USER%
project_NAME=%project_NAME%

PATHDIR_home_user_root=%PATHDIR_home_user_root%
PATHDIR_home_user=%PATHDIR_home_user%

PATHDIR_root_third=%PATHDIR_root_third%
PATHDIR_root_repositories=%PATHDIR_root_repositories%'''
            .replace('%USER%', str(self.USER()))
            .replace('%project_NAME%', str(self.project_NAME()))
            \
            .replace('%PATHDIR_home_user_root%', str(self.PATHDIR_home_user_root()))
            .replace('%PATHDIR_home_user%', str(self.PATHDIR_home_user()))
            .replace('%PATHDIR_root_third%', str(self.PATHDIR_root_third()))
            .replace('%PATHDIR_root_repositories%', str(self.PATHDIR_root_repositories()))
        )
        logger.info('[deployer] Resolve common paths!')

        logger.info('[deployer] Make common dirs...')
        self.PATHDIR_root_repositories().mkdir(parents=True)
        self.PATHDIR_root_third().mkdir(parents=True)
        logger.info('[deployer] Make common dirs!')

        logger.info('[deployer] Process common!')


    # sitedeployer:
    def PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy(self) -> Path:
        return self._PATHFILE_deploypy

    def PATHDIR_home_user_root_sitedeployer_sitedeployerpackage(self) -> Path:
        return self.PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy().parent

    def PATHDIR_home_user_root_sitedeployer(self) -> Path:
        return self.PATHDIR_home_user_root_sitedeployer_sitedeployerpackage().parent

    def process_sitedeployer(self) -> None:
        logger.info('[deployer] Process sitedeployer...')

        logger.info('[deployer] Resolve sitedeployer paths...')

        logger.info(
'''PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy=%PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy%
PATHDIR_home_user_root_sitedeployer_sitedeployerpackage=%PATHDIR_home_user_root_sitedeployer_sitedeployerpackage%
PATHDIR_home_user_root_sitedeployer=%PATHDIR_home_user_root_sitedeployer%'''
                .replace('%PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy%',
                         str(self.PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy()))
                .replace('%PATHDIR_home_user_root_sitedeployer_sitedeployerpackage%',
                         str(self.PATHDIR_home_user_root_sitedeployer_sitedeployerpackage()))
                .replace('%PATHDIR_home_user_root_sitedeployer%', str(self.PATHDIR_home_user_root_sitedeployer()))
        )

        logger.info('[deployer] Resolve sitedeployer paths!')

        logger.info('[deployer] Process sitedeployer!')


    # third:
    def URL_baserepository(self) -> str:
        return '''git@github.com:ynsight/base.git'''

    def PATHDIR_root_repositories_baserepository(self) -> Path:
        return self.PATHDIR_root_repositories() / 'base'

    def PATHDIR_root_repositories_baserepository_basepackage(self) -> Path:
        return self.PATHDIR_root_repositories_baserepository() / 'src/ins/lib/base'

    def PATHDIR_root_third_basepackage(self) -> Path:
        return self.PATHDIR_root_third() / 'base'



    def process_third(self) -> None:
        logger.info('[deployer] Process third...')

        logger.info(
'''base paths:
URL_baserepository=%URL_baserepository%
PATHDIR_root_repositories_baserepository=%PATHDIR_root_repositories_baserepository%
PATHDIR_root_repositories_baserepository_basepackage=%PATHDIR_root_repositories_baserepository_basepackage%
PATHDIR_root_third_basepackage=%PATHDIR_root_third_basepackage%'''
            .replace('%URL_baserepository%', str(self.URL_baserepository()))
            .replace('%PATHDIR_root_repositories_baserepository%', str(self.PATHDIR_root_repositories_baserepository()))
            .replace('%PATHDIR_root_repositories_baserepository_basepackage%', str(self.PATHDIR_root_repositories_baserepository_basepackage()))
            .replace('%PATHDIR_root_third_basepackage%', str(self.PATHDIR_root_third_basepackage()))
        )

        logger.info('[deployer] Install base...')

        subprocess.run(
            ['git', 'clone', self.URL_baserepository()],
            cwd=str(self.PATHDIR_root_repositories())
        )
        if self.PATHDIR_root_repositories_baserepository().is_dir():
            shutil.copytree(
                self.PATHDIR_root_repositories_baserepository_basepackage(),
                self.PATHDIR_root_third_basepackage()
            )
        logger.info('[deployer] Install base!')

        logger.info('[deployer] Process third!')



    # project:
    def PATHDIR_root_repositories_projectrepository(self) -> Path:
        return self.PATHDIR_root_repositories() / self.project_NAME()

    def URL_projectrepository(self) -> str:
        return '''git@github.com:ynsight/%project_NAME%.git'''\
            .replace('%project_NAME%', self.project_NAME())

    def process_project(self) -> None:
        logger.info('[deployer] Process project...')

        logger.info(
'''project paths:
project_NAME=%project_NAME%
URL_projectrepository=%URL_projectrepository%
PATHDIR_root_repositories_projectrepository=%PATHDIR_root_repositories_projectrepository%'''
            .replace('%project_NAME%', str(self.project_NAME()))
            .replace('%URL_projectrepository%', str(self.URL_projectrepository()))
            .replace('%PATHDIR_root_repositories_projectrepository%', str(self.PATHDIR_root_repositories_projectrepository()))
        )


        logger.info('[deployer] Downloading project repository...')
        subprocess.run(
            ['git', 'clone', self.URL_projectrepository()],
            cwd=str(self.PATHDIR_root_repositories())
        )
        logger.info('[deployer] Downloading project repository!')

        logger.info('[deployer] Process project!')



    # site:
    def PATHDIR_root_site(self) -> Path:
        return self.PATHDIR_home_user_root() / 'site'

    def PATHDIR_root_site_lib(self) -> Path:
        return self.PATHDIR_root_site() / 'lib'

    def PATHDIR_root_site_lib_sitepackage(self) -> Path:
        return self.PATHDIR_root_site_lib() / self.sitepackage()

    def PATHDIR_root_repositories_projectrepository_site(self) -> Path:
        return self.PATHDIR_root_repositories_projectrepository() / 'src/site'

    def process_site(self) -> None:
        logger.info('[deployer] Process site...')

        logger.info(
'''site paths:
sitepackage=%sitepackage%
URL_site=%URL_site%
PATHDIR_root_site=%PATHDIR_root_site%
PATHDIR_root_site_lib=%PATHDIR_root_site_lib%
PATHDIR_root_site_lib_sitepackage=%PATHDIR_root_site_lib_sitepackage%

PATHDIR_root_repositories_projectrepository_site=%PATHDIR_root_repositories_projectrepository_site%'''
            .replace('%sitepackage%', str(self.sitepackage()))
            .replace('%URL_site%', str(self.URL_site()))
            .replace('%URL_projectrepository%', str(self.URL_projectrepository()))
\
            .replace('%PATHDIR_root_site%', str(self.PATHDIR_root_site()))
            .replace('%PATHDIR_root_site_lib%', str(self.PATHDIR_root_site_lib()))
            .replace('%PATHDIR_root_site_lib_sitepackage%', str(self.PATHDIR_root_site_lib_sitepackage()))
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
        return self.PATHDIR_home_user_root() / 'doc'

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
                '/var/www/%USER%_pythonanywhere_com_wsgi.py'
                    .replace('%USER%', self.USER())
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

project_home = u'/home/%USER%/root/site/lib'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

sys.path = [/home/%USER%/root/doc/lib] + sys.path
sys.path = [/home/%USER%/root/third] + sys.path

from %sitepackage%.main import app as application
'''

        self.PATHFILE_wsgipy().write_text(
            wsgipy_template
                .replace('%USER%', self.USER())
                .replace('%sitepackage%', self.sitepackage())
        )
        logger.info('[deployer] Write wsgi.py file!')

        logger.info('[deployer] Process wsgi.py!')



    # update.py:
    def PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy(self) -> Path:
        return self.PATHDIR_home_user_root_sitedeployer_sitedeployerpackage() / 'update.py'

    def PATHFILE_home_user_updatepy(self) -> Path:
        return self.PATHDIR_home_user() / 'update.py'

    def process_updatepy(self) -> None:
        logger.info('[deployer] Process update.py...')

        logger.info(
'''update.py paths:
PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy=%PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy%
PATHFILE_home_user_updatepy=%PATHFILE_home_user_updatepy%'''
            .replace('%PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy%', str(self.PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy()))
            .replace('%PATHFILE_home_user_updatepy%', str(self.PATHFILE_home_user_updatepy()))
        )

        logger.info('[deployer] Write update.py file...')
        shutil.copyfile(
            self.PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy(),
            self.PATHFILE_home_user_updatepy()
        )
        logger.info('[deployer] Write update.py file!')
        logger.info('[deployer] Process update.py!')


    def Execute(self) -> None:
        self.process_common()
        self.process_sitedeployer()
        self.process_third()
        self.process_project()
        self.process_site()
        self.process_doc()
        self.process_wsgipy()
        self.process_updatepy()




class Project_Sitedeployer(
    Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def deploy_doc(self) -> None:
        pass

    def Execute(self) -> None:
        Sitedeployer.Execute(self)
        self.deploy_doc()


# sola:
class sola_Sitedeployer(
    Project_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Project_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def project_NAME(self) -> str:
        return 'sola'

    def USER(self) -> str:
        return 'getsola'



# base:
class base_Sitedeployer(
    Project_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Project_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def project_NAME(self) -> str:
        return 'base'

    def USER(self) -> str:
        return 'getbase'



# myrta:
class myrta_Sitedeployer(
    Project_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Project_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def project_NAME(self) -> str:
        return 'myrta'

    def USER(self) -> str:
        return 'getmyrta'



# una:
class una_Sitedeployer(
    Project_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Project_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def project_NAME(self) -> str:
        return 'una'

    def USER(self) -> str:
        return 'getuna'



# rs:
class rs_Sitedeployer(
    Project_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Project_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def project_NAME(self) -> str:
        return 'rs'

    def USER(self) -> str:
        return 'getrs'



# fw:
class fw_Sitedeployer(
    Project_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Project_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def project_NAME(self) -> str:
        return 'fw'

    def USER(self) -> str:
        return 'getfw'



# Ln:
class Ln_Sitedeployer(
    Project_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Project_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def project_NAME(self) -> str:
        return 'Ln'

    def USER(self) -> str:
        return 'getln'



# project:
class project_Sitedeployer(
    Project_Sitedeployer
):
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Project_Sitedeployer.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def project_NAME(self) -> str:
        return 'project'

    def USER(self) -> str:
        return 'getprojekt'



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

    def project_NAME(self) -> str:
        return 'ynsight'

    def USER(self) -> str:
        return 'ynsight'



def Sitedeployer__from__PATHFILE_deploypy(
    PATHFILE_deploypy:Path=None
) -> Sitedeployer:
    USER = PATHFILE_deploypy.parent.parent.parent.parent.name
    return {
        'getsola': sola_Sitedeployer,
        'getbase': base_Sitedeployer,
        'getmyrta': myrta_Sitedeployer,
        'getuna': una_Sitedeployer,
        'getrs': rs_Sitedeployer,
        'getfw': fw_Sitedeployer,
        'getln': Ln_Sitedeployer,
        'getprojekt': project_Sitedeployer,
        'ynsight': ynsight_Sitedeployer
    }[USER](
        PATHFILE_deploypy=PATHFILE_deploypy
    )



if __name__ == '__main__':
    logger.info('[deployer] Deploy site...')

    Sitedeployer__from__PATHFILE_deploypy(
        PATHFILE_deploypy=Path(sys.argv[0])
    ).Execute()

    logger.info('[deployer] Deploy site!')
