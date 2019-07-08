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

    def deploy_common(self) -> None:
        PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy = self._PATHFILE_deploypy
        PATHDIR_home_user_root_sitedeployer_sitedeployerpackage = PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy.parent
        PATHDIR_home_user_root_sitedeployer = PATHDIR_home_user_root_sitedeployer_sitedeployerpackage.parent
        PATHDIR_home_user_root = PATHDIR_home_user_root_sitedeployer.parent
        PATHDIR_home_user = PATHDIR_home_user_root.parent

        PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy = PATHDIR_home_user_root_sitedeployer_sitedeployerpackage / 'update.py'
        PATHFILE_home_user_updatepy = PATHDIR_home_user / 'update.py'

        USER = PATHDIR_home_user.name

        project = {
            'getsola':    'sola',
            'getbase':    'base',
            'getmyrta':   'myrta',
            'getuna':     'una',
            'getrs':      'rs',
            'getfw':      'fw',
            'getln':      'Ln',
            'ynsight':    'ynsight',
            'getprojekt': 'project'
        }[USER]

        sitepackage = 'site_' + project
        URL_site = USER + '.pythonanywhere.com'
        URL_projectrepository = '''https://github.com/solaris6/%project%.git'''\
            .replace('%project%', project)
        PATHDIR_root_site = PATHDIR_home_user_root / '_site'
        PATHDIR_root_site_sitepackage = PATHDIR_root_site / sitepackage

        docpackage = 'doc_' + project
        PATHDIR_root_doc = PATHDIR_home_user_root / '_doc'
        PATHDIR_root_doc_docpackage = PATHDIR_root_doc / docpackage

        PATHDIR_root_third = PATHDIR_home_user_root / 'third'

        PATHDIR_root_repositories = PATHDIR_home_user_root / 'repositories'
        PATHDIR_root_repositories_projectrepository = PATHDIR_root_repositories / project

        PATHDIR_root_repositories_projectrepository_site = PATHDIR_root_repositories_projectrepository / '_site'
        PATHDIR_root_repositories_projectrepository_site_sitepackage = PATHDIR_root_repositories_projectrepository_site / sitepackage

        PATHDIR_root_repositories_projectrepository_doc = PATHDIR_root_repositories_projectrepository / '_doc'
        PATHDIR_root_repositories_projectrepository_doc_docpackage = PATHDIR_root_repositories_projectrepository_doc / docpackage

        PATHFILE_wsgipy = Path(
            '/var/www/%USER%_pythonanywhere_com_wsgi.py'
                .replace('%USER%', USER)
        )

        logger.info(
'''PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy=%PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy%
PATHDIR_home_user_root_sitedeployer_sitedeployerpackage=%PATHDIR_home_user_root_sitedeployer_sitedeployerpackage%
PATHDIR_home_user_root_sitedeployer=%PATHDIR_home_user_root_sitedeployer%
PATHDIR_home_user_root=%PATHDIR_home_user_root%
PATHDIR_home_user=%PATHDIR_home_user%

PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy=%PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy%
PATHFILE_home_user_updatepy=%PATHFILE_home_user_updatepy%

USER=%USER%
project=%project%
sitepackage=%sitepackage%
URL_site=%URL_site%
URL_projectrepository=%URL_projectrepository%
PATHDIR_root_site=%PATHDIR_root_site%
PATHDIR_root_site_sitepackage=%PATHDIR_root_site_sitepackage%

docpackage=%docpackage%
PATHDIR_root_doc=%PATHDIR_root_doc%
PATHDIR_root_doc_docpackage=%PATHDIR_root_doc_docpackage%

PATHDIR_root_third=%PATHDIR_root_third%

PATHDIR_root_repositories=%PATHDIR_root_repositories%
PATHDIR_root_repositories_projectrepository=%PATHDIR_root_repositories_projectrepository%

PATHDIR_root_repositories_projectrepository_site=%PATHDIR_root_repositories_projectrepository_site%
PATHDIR_root_repositories_projectrepository_site_sitepackage=%PATHFILE_root_repositories_projectrepository_site_sitepackage_updatepy%

PATHDIR_root_repositories_projectrepository_doc=%PATHDIR_root_repositories_projectrepository_doc%
PATHDIR_root_repositories_projectrepository_doc_docpackage=%PATHDIR_root_repositories_projectrepository_doc_docpackage%

PATHFILE_wsgipy=%PATHFILE_wsgipy%'''
            .replace('%PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy%', str(PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_deploypy))
            .replace('%PATHDIR_home_user_root_sitedeployer_sitedeployerpackage%', str(PATHDIR_home_user_root_sitedeployer_sitedeployerpackage))
            .replace('%PATHDIR_home_user_root_sitedeployer%', str(PATHDIR_home_user_root_sitedeployer))
            .replace('%PATHDIR_home_user_root%', str(PATHDIR_home_user_root))
            .replace('%PATHDIR_home_user%', str(PATHDIR_home_user))
            \
            .replace('%PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy%', str(PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy))
            .replace('%PATHFILE_home_user_updatepy%', str(PATHFILE_home_user_updatepy))
            \
            .replace('%USER%', str(USER))
            .replace('%project%', str(project))
            .replace('%sitepackage%', str(sitepackage))
            .replace('%URL_site%', str(URL_site))
            .replace('%URL_projectrepository%', str(URL_projectrepository))
            .replace('%PATHDIR_root_site%', str(PATHDIR_root_site))
            .replace('%PATHDIR_root_site_sitepackage%', str(PATHDIR_root_site_sitepackage))
            \
            .replace('%docpackage%', str(docpackage))
            .replace('%PATHDIR_root_doc%', str(PATHDIR_root_doc))
            .replace('%PATHDIR_root_doc_docpackage%', str(PATHDIR_root_doc_docpackage))
            \
            .replace('%PATHDIR_root_third%', str(PATHDIR_root_third))
            \
            .replace('%PATHDIR_root_repositories%', str(PATHDIR_root_repositories))
            .replace('%PATHDIR_root_repositories_projectrepository%', str(PATHDIR_root_repositories_projectrepository))
            \
            .replace('%PATHDIR_root_repositories_projectrepository_site%', str(PATHDIR_root_repositories_projectrepository_site))
            .replace('%PATHDIR_root_repositories_projectrepository_site_sitepackage%', str(PATHDIR_root_repositories_projectrepository_site_sitepackage))
            \
            .replace('%PATHDIR_root_repositories_projectrepository_doc%', str(PATHDIR_root_repositories_projectrepository_doc))
            .replace('%PATHDIR_root_repositories_projectrepository_doc_docpackage%', str(PATHDIR_root_repositories_projectrepository_doc_docpackage))
            \
            .replace('%PATHFILE_wsgipy%', str(PATHFILE_wsgipy))
        )

        PATHDIR_root_repositories.mkdir(parents=True)



        logger.info('[deployer] Setup project dependencies...')
        PATHDIR_root_third.mkdir()
        logger.info('[deployer] Setup project dependencies!')



        logger.info('[deployer] Install base...')
        URL_baserepository = '''https://github.com/solaris6/base.git'''\
            .replace('%project%', project)
        PATHDIR_root_repositories_baserepository = PATHDIR_root_repositories / 'base'
        PATHDIR_root_repositories_baserepository_basepackage = PATHDIR_root_repositories_baserepository / 'src/ins/lib/base'

        subprocess.run(
            ['git', 'clone', URL_baserepository],
            cwd=str(PATHDIR_root_repositories)
        )
        if PATHDIR_root_repositories_baserepository.is_dir():
            shutil.copytree(
                PATHDIR_root_repositories_baserepository_basepackage,
                PATHDIR_root_third
            )
        logger.info('[deployer] Install base!')



        logger.info('[deployer] Downloading project repository...')
        subprocess.run(
            ['git', 'clone', URL_projectrepository],
            cwd=str(PATHDIR_root_repositories)
        )
        logger.info('[deployer] Downloading project repository!')



        logger.info('[deployer] Install project site...')
        if PATHDIR_root_repositories_projectrepository.is_dir():
            shutil.copytree(
                PATHDIR_root_repositories_projectrepository_site,
                PATHDIR_root_site
            )
        logger.info('[deployer] Install project site!')



        logger.info('[deployer] Install project doc...')
        if PATHDIR_root_repositories_projectrepository.is_dir():
            shutil.copytree(
                PATHDIR_root_repositories_projectrepository_doc,
                PATHDIR_root_doc
            )
        logger.info('[deployer] Install project doc!')



        logger.info('[deployer] Write wsgi.py...')
        wsgipy_template = \
'''import sys

project_home = u'/home/%USER%/root/_site'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

sys.path = [/home/%USER%/root/_site] + sys.path
sys.path = [/home/%USER%/root/_doc] + sys.path
sys.path = [/home/%USER%/root/third] + sys.path

from %sitepackage%.main import app as application
'''

        PATHFILE_wsgipy.write_text(
            wsgipy_template
                .replace('%USER%', USER)
                .replace('%sitepackage%', sitepackage)
        )

        logger.info('[deployer] Write wsgi.py!')



        logger.info('[deployer] Write updater...')
        shutil.copyfile(
            PATHFILE_home_user_root_sitedeployer_sitedeployerpackage_updatepy,
            PATHFILE_home_user_updatepy
        )
        logger.info('[deployer] Write updater!')


    def Execute(self) -> None:
        self.deploy_common()


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
