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
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

class Sitedeployer:
    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        self._PATHFILE_deploypy = PATHFILE_deploypy
        self._PATH_old = None
        self._PYTHONPATH_old = None
        self._ynsight_projects_installed = []


    @staticmethod
    def environment_report() -> Dict[str,Any]:
        result = {}
        result['cwd'] = os.getcwd()
        # result['env_vars'] = dict(os.environ)
        result['PATH'] = os.environ['PATH'].split(os.pathsep) if 'PATH' in os.environ else []
        result['PYTHONPATH'] = os.environ['PYTHONPATH'].split(os.pathsep) if 'PYTHONPATH' in os.environ else []
        return result

    def log_environment(self) -> None:
        logger.info(
            json.dumps({
                'environment_report': self.environment_report()
                }, indent=2
            )
        )


    @staticmethod
    def pythonanywhere_username() -> str:
        raise NotImplementedError("")

    @classmethod
    def URL_site(cls) -> str:
        return cls.pythonanywhere_username() + '.pythonanywhere.com'

    def PATHDIR_home_pythonanywhereusername_root(self) -> Path:
        return self._PATHFILE_deploypy.parent.parent.parent

    def PATHDIR_home_pythonanywhereusername(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root().parent

    def PATHDIR_root_repositories(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'repositories'

    def PATHDIR_root_build(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'build'

    def PATHDIR_root_buildtemp(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'buildtemp'

    def PATHDIR_root_ins(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'ins'

    def PATHDIR_root_instemp(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / 'instemp'

    def PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy(self) -> Path:
        return self._PATHFILE_deploypy

    def PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage(self) -> Path:
        return self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy().parent

    def PATHDIR_home_pythonanywhereusername_root_sitedeployer(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage().parent

    def process_common(self) -> None:
        logger.info('Process common...')

        logger.info('Resolve common paths...')
        logger.info(
'''pythonanywhere_username=%pythonanywhere_username%
project_NAME=%project_NAME%
projektorworkshop_projektorworkshopsitepubflaskpackage=%projektorworkshop_projektorworkshopsitepubflaskpackage%
URL_site=%URL_site%

PATHDIR_home_pythonanywhereusername_root=%PATHDIR_home_pythonanywhereusername_root%
PATHDIR_home_pythonanywhereusername=%PATHDIR_home_pythonanywhereusername%

PATHDIR_root_repositories=%PATHDIR_root_repositories%
PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy=%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy%
PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage=%PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage%
PATHDIR_home_pythonanywhereusername_root_sitedeployer=%PATHDIR_home_pythonanywhereusername_root_sitedeployer%'''
            .replace('%pythonanywhere_username%', str(self.pythonanywhere_username()))
            .replace('%project_NAME%', str(self.project_NAME()))
            .replace('%projektorworkshop_projektorworkshopsitepubflaskpackage%', str(self.projektorworkshop_projektorworkshopsitepubflaskpackage()))
            .replace('%URL_site%', str(self.URL_site()))
            \
            .replace('%PATHDIR_home_pythonanywhereusername_root%', str(self.PATHDIR_home_pythonanywhereusername_root()))
            .replace('%PATHDIR_home_pythonanywhereusername%', str(self.PATHDIR_home_pythonanywhereusername()))
            .replace('%PATHDIR_root_repositories%', str(self.PATHDIR_root_repositories()))
            .replace('%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy%',
                     str(self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_deploypy()))
            .replace('%PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage%',
                     str(self.PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage()))
            .replace('%PATHDIR_home_pythonanywhereusername_root_sitedeployer%', str(self.PATHDIR_home_pythonanywhereusername_root_sitedeployer()))
        )
        logger.info('Resolve common paths!')

        logger.info('Make common dirs...')
        self.PATHDIR_root_repositories().mkdir(parents=True)
        self.PATHDIR_root_build().mkdir(parents=True)
        self.PATHDIR_root_buildtemp().mkdir(parents=True)
        self.PATHDIR_root_ins().mkdir(parents=True)
        self.PATHDIR_root_instemp().mkdir(parents=True)
        logger.info('Make common dirs!')

        logger.info('Process common!')


    # temp ynsight dependencies:
    @staticmethod
    def temp_ynsight_dependencies() -> List[Type['Projekt_Sitedeployer']]:
        from deployers.Projekt.base_ProjektSitedeployer import base_ProjektSitedeployer
        from deployers.Projekt.projekt_ProjektSitedeployer import projekt_ProjektSitedeployer
        from deployers.Projekt.myrta_ProjektSitedeployer import myrta_ProjektSitedeployer
        return [
            base_ProjektSitedeployer,
            projekt_ProjektSitedeployer,
            myrta_ProjektSitedeployer
        ]

    def process_temp_ynsight_dependency(self,
        temp_ynsight_project:'Projekt_Sitedeployer'=None
    ) -> None:
        logger.info('Process temp_ynsight_project: "%temp_ynsight_project%"...'.replace('%temp_ynsight_project%', temp_ynsight_project.project_NAME()))
        temp_ynsight_project.clonebuildinstalltemp_project()
        subprocess.run(['projekt'], shell=True)
        subprocess.run(['myrta'], shell=True)
        subprocess.run(['agent'], shell=True)
        logger.info('Process temp_ynsight_project: "%temp_ynsight_project%"!'.replace('%temp_ynsight_project%', temp_ynsight_project.project_NAME()))

    def process_temp_ynsight_dependencies(self) -> None:
        logger.info('Process temp ynsight dependencies...')
        for temp_ynsight_dependency in self.temp_ynsight_dependencies():
            self.process_temp_ynsight_dependency(
                temp_ynsight_project=temp_ynsight_dependency(
                    PATHFILE_deploypy=self._PATHFILE_deploypy
                )
            )

        logger.info('Process temp ynsight dependencies!')



    # ynsight dependencies:
    @staticmethod
    def ynsight_dependencies_common() -> List[Type['Sitedeployer']]:
        from deployers.Projekt.base_ProjektSitedeployer import base_ProjektSitedeployer
        from deployers.Projekt.projekt_ProjektSitedeployer import projekt_ProjektSitedeployer
        from deployers.Projekt.myrta_ProjektSitedeployer import myrta_ProjektSitedeployer
        return [
            base_ProjektSitedeployer,
            projekt_ProjektSitedeployer,
            myrta_ProjektSitedeployer
        ]

    @staticmethod
    def ynsight_dependencies_self() -> List[Type['Sitedeployer']]:
        raise NotImplementedError("")

    @classmethod
    def ynsight_dependencies_all(cls) -> List[Type['Sitedeployer']]:
        raise NotImplementedError("")

    def process_ynsight_dependencies(self) -> None:
        logger.info('Process ynsight dependencies...')
        for ynsight_dependency in self.ynsight_dependencies_all():

            ynsight_dependency=ynsight_dependency(
                PATHFILE_deploypy=self._PATHFILE_deploypy
            )
            logger.info('Clonebuildinstall ynsight project: "%ynsight_project%"...'.replace('%ynsight_project%', ynsight_dependency.project_NAME()))
            if not ynsight_dependency.project_NAME() in self._ynsight_projects_installed:
                self._ynsight_projects_installed.append(ynsight_dependency.project_NAME())
                ynsight_dependency.clonebuildinstall_project()
            logger.info('Clonebuildinstall ynsight project: "%ynsight_project%"!'.replace('%ynsight_project%', ynsight_dependency.project_NAME()))

        logger.info('Test ynsight dependencies...')
        subprocess.run(['projekt'], shell=True)
        subprocess.run(['myrta'], shell=True)
        subprocess.run(['agent'], shell=True)
        logger.info('Test ynsight dependencies!')

        logger.info('Process ynsight dependencies!')



    # process project:
    @staticmethod
    def project_NAME() -> str:
        raise NotImplementedError("")

    @staticmethod
    def github_username() -> str:
        return 'ynsight'

    @staticmethod
    def github_url_type() -> str:
        raise NotImplementedError("")


    def PATHDIR_root_repositories_projectrepository(self) -> Path:
        return self.PATHDIR_root_repositories() / self.project_NAME()


    def PATHDIR_root_build_project(self) -> Path:
        return self.PATHDIR_root_build() / self.project_NAME()

    def PATHDIR_root_buildtemp_project(self) -> Path:
        return self.PATHDIR_root_buildtemp() / self.project_NAME()

    def PATHDIR_root_ins_project(self) -> Path:
        return self.PATHDIR_root_ins() / self.project_NAME()

    def PATHDIR_root_instemp_project(self) -> Path:
        return self.PATHDIR_root_instemp() / self.project_NAME()


    @classmethod
    def URLSSH_github_project_repository(cls) -> str:
        return '''git@github.com:%github_username%/%project_NAME%.git''' \
            .replace('%project_NAME%', cls.project_NAME()) \
            .replace('%github_username%', cls.github_username())

    @classmethod
    def URLHTTP_github_project_repository(cls) -> str:
        return '''http://github.com/%github_username%/%project_NAME%.git''' \
            .replace('%project_NAME%', cls.project_NAME()) \
            .replace('%github_username%', cls.github_username())

    @classmethod
    def URLHTTPS_github_project_repository(cls) -> str:
        return '''https://github.com/%github_username%/%project_NAME%.git''' \
            .replace('%project_NAME%', cls.project_NAME()) \
            .replace('%github_username%', cls.github_username())

    @classmethod
    def URL_github_project_repository(cls) -> str:
        result = None
        if cls.github_url_type() == 'ssh':
            result = cls.URLSSH_github_project_repository()
        elif cls.github_url_type() == 'http':
            result = cls.URLHTTP_github_project_repository()
        elif cls.github_url_type() == 'https':
            result = cls.URLHTTPS_github_project_repository()
        return result


    def clone_project(self) -> None:
        logger.info('Clone "%project%" repository...'.replace('%project%', self.project_NAME()))
        if not self.PATHDIR_root_repositories_projectrepository().is_dir():
            subprocess.run(
                ['git', 'clone', self.URL_github_project_repository()],
                cwd=str(self.PATHDIR_root_repositories())
            )
            logger.info('Clone "%project%" repository!'.replace('%project%', self.project_NAME()))



    def clonebuildinstalltemp_project(self) -> None:
        logger.info('Clone/Build/Install "%project%" temp project...'.replace('%project%', self.project_NAME()))
        self.log_environment()

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.project_NAME()))
        PATHDIR_root_repositories_projectrepository_ins = self.PATHDIR_root_repositories_projectrepository() / 'src/ins'

        if PATHDIR_root_repositories_projectrepository_ins.is_dir() and not self.PATHDIR_root_instemp_project().is_dir():
            shutil.copytree(
                PATHDIR_root_repositories_projectrepository_ins,
                self.PATHDIR_root_instemp_project()
            )

        os.environ['PATH'] = str(self.PATHDIR_root_instemp_project() / 'bin') + os.pathsep + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
        os.environ['PYTHONPATH'] = str(self.PATHDIR_root_instemp_project() / 'lib') + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')

        logger.info('Build and Install ("%project%")'.replace('%project%', self.project_NAME()))

        self.log_environment()
        logger.info('Clone/Build/Install "%project%" temp project!'.replace('%project%', self.project_NAME()))



    def clonebuildinstall_project(self) -> None:
        logger.info('Clone/Build/Install "%project%" project...'.replace('%project%', self.project_NAME()))
        self.log_environment()

        self.clone_project()

        logger.info('Build and Install ("%project%")'.replace('%project%', self.project_NAME()))
        PATHDIR_root_repositories_projectrepository_ins = self.PATHDIR_root_repositories_projectrepository() / 'src/ins'

        if PATHDIR_root_repositories_projectrepository_ins.is_dir() and not self.PATHDIR_root_ins_project().is_dir():
            shutil.copytree(
                PATHDIR_root_repositories_projectrepository_ins,
                self.PATHDIR_root_ins_project()
            )

        os.environ['PATH'] = str(self.PATHDIR_root_ins_project() / 'bin') + os.pathsep + ((os.pathsep + os.environ['PATH']) if 'PATH' in os.environ else '')
        os.environ['PYTHONPATH'] = str(self.PATHDIR_root_ins_project() / 'lib') + ((os.pathsep + os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else '')

        if self.PATHDIR_root_instemp_project().is_dir():
            shutil.rmtree(self.PATHDIR_root_instemp_project())

        logger.info('Build and Install ("%project%")!'.replace('%project%', self.project_NAME()))

        self.log_environment()
        logger.info('Clone/Build/Install "%project%" project!'.replace('%project%', self.project_NAME()))



    # projektorworkshop:
    @staticmethod
    def projektorworkshop_Type() -> str:
        raise NotImplementedError("")

    @classmethod
    def projektorworkshop_projektorworkshopsitepubflaskpackage(cls) -> str:
        return cls.projektorworkshop_Type() + 'sitepub_' + cls.project_NAME()

    @classmethod
    def projektorworkshop_package(cls) -> str:
        return cls.projektorworkshop_Type() + '_' + cls.project_NAME()
    
    def PATHDIR_root_repositories_projectrepository_projektorworkshop(self) -> Path:
        return self.PATHDIR_root_repositories_projectrepository() / ('_' + self.projektorworkshop_Type())


    def PATHDIR_root_projektorworkshop(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root() / ('_' + self.projektorworkshop_Type())

    def PATHDIR_root_projektorworkshop_projektorworkshoppackage(self) -> Path:
        return self.PATHDIR_root_projektorworkshop() / self.projektorworkshop_package()

    def PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage(self) -> Path:
        return self.PATHDIR_root_projektorworkshop() / self.projektorworkshop_projektorworkshopsitepubflaskpackage()


    def process_projektorworkshop(self) -> None:
        logger.info('Process projektorworkshop...')
        logger.info(
'''# projektorworkshop paths:
PATHDIR_root_repositories_projectrepository_projektorworkshop=%PATHDIR_root_repositories_projectrepository_projektorworkshop%

PATHDIR_root_projektorworkshop=%PATHDIR_root_projektorworkshop%
PATHDIR_root_projektorworkshop_projektorworkshoppackage=%PATHDIR_root_projektorworkshop_projektorworkshoppackage%
PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage=%PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage%'''

            .replace('%PATHDIR_root_repositories_projectrepository_projektorworkshop%', str(self.PATHDIR_root_repositories_projectrepository_projektorworkshop()))
            .replace('%PATHDIR_root_projektorworkshop%', str(self.PATHDIR_root_projektorworkshop()))
            .replace('%PATHDIR_root_projektorworkshop_projektorworkshoppackage%', str(self.PATHDIR_root_projektorworkshop_projektorworkshoppackage()))
            .replace('%PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage%', str(self.PATHDIR_root_projektorworkshop_projektorworkshopsitepubflaskpackage()))
        )

        logger.info('Install projektorworkshop...')
        if self.PATHDIR_root_repositories_projectrepository().is_dir():
            shutil.copytree(
                self.PATHDIR_root_repositories_projectrepository_projektorworkshop(),
                self.PATHDIR_root_projektorworkshop()
            )
        logger.info('Install projektorworkshop!')
        logger.info('Process projektorworkshop!')




    # wsgi.py:
    def PATHFILE_wsgipy(self) -> Path:
        return Path(
                '/var/www/%pythonanywhere_username%_pythonanywhere_com_wsgi.py'
                    .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            )

    def process_wsgipy(self) -> None:
        logger.info('Process wsgi.py...')

        logger.info(
'''wsgi.py paths:
PATHFILE_wsgipy=%PATHFILE_wsgipy%'''
            .replace('%PATHFILE_wsgipy%', str(self.PATHFILE_wsgipy()))
        )

        logger.info('Write wsgi.py file...')
        wsgipy_template = \
'''import sys, os
from pathlib import Path

PATHDIR_projektorworkshop = Path('/home/%pythonanywhere_username%/root/_%projektorworkshop%')
if not str(PATHDIR_projektorworkshop) in sys.path:
    sys.path = [str(PATHDIR_projektorworkshop)] + sys.path


# Append ynsight project`s packages to sys.paths:
%ynsight_projects_packages_syspaths_appends%

# Append ynsight project`s executables to PATH envvar:
%ynsight_projects_packages_PATH_appends%

from %projektorworkshop_projektorworkshopsitepubflaskpackage%.flask_app import app as application
'''

        ynsight_projects_packages_syspaths_appends = ''
        ynsight_projects_packages_PATH_appends = ''
        for i,ynsight_project_installed in enumerate(self._ynsight_projects_installed):
            ynsight_projects_packages_syspaths_appends += ('' if i==0 else '\n') +\
"os.environ['PATH'] += os.pathsep + '/home/%pythonanywhere_username%/root/ins/%dependency_NAME%/bin'"\
    .replace('%dependency_NAME%', ynsight_project_installed.project_NAME())

            ynsight_projects_packages_PATH_appends += ('' if i==0 else '\n') +\
"sys.path = ['/home/%pythonanywhere_username%/root/ins/%dependency_NAME%/lib'] + sys.path"\
    .replace('%dependency_NAME%', ynsight_project_installed.project_NAME())

        wsgipy_fc = wsgipy_template\
            .replace('%ynsight_projects_packages_syspaths_appends%', ynsight_projects_packages_syspaths_appends)\
            .replace('%ynsight_projects_packages_PATH_appends%', ynsight_projects_packages_PATH_appends)\
            .replace('%pythonanywhere_username%', self.pythonanywhere_username())\
            .replace('%projektorworkshop_projektorworkshopsitepubflaskpackage%', self.projektorworkshop_projektorworkshopsitepubflaskpackage())\
            .replace('%projektorworkshop%', self.projektorworkshop_Type())

        self.PATHFILE_wsgipy().write_text(
            wsgipy_fc
        )

        logger.info('WSGIPY_FILE_BEGIN[[[' + wsgipy_fc + ']]]WSGIPY_FILE_END')
        logger.info('Write wsgi.py file!')

        logger.info('Process wsgi.py!')



    # update.py:
    def PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage() / 'update.py'

    def PATHFILE_home_pythonanywhereusername_updatepy(self) -> Path:
        return self.PATHDIR_home_pythonanywhereusername() / 'update.py'

    def process_updatepy(self) -> None:
        logger.info('Process update.py...')

        logger.info(
'''update.py paths:
PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy=%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy%
PATHFILE_home_pythonanywhereusername_updatepy=%PATHFILE_home_pythonanywhereusername_updatepy%'''
            .replace('%PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy()))
            .replace('%PATHFILE_home_pythonanywhereusername_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_updatepy()))
        )

        logger.info('Write update.py file...')
        shutil.copyfile(
            self.PATHFILE_home_pythonanywhereusername_root_sitedeployer_sitedeployerpackage_updatepy(),
            self.PATHFILE_home_pythonanywhereusername_updatepy()
        )
        logger.info('Write update.py file!')

        logger.info('Process update.py!')

    def Execute_PRE(self) -> None:
        self.log_environment()
        self.process_common()

        self.log_environment()
        self._PATH_old = copy(os.environ['PATH']) if 'PATH' in os.environ else ''
        self._PYTHONPATH_old = copy(os.environ['PYTHONPATH']) if 'PYTHONPATH' in os.environ else ''
        self.log_environment()

        self.process_temp_ynsight_dependencies()

        self.process_ynsight_dependencies()
        self.clonebuildinstall_project()
        self.process_projektorworkshop()


    def Execute(self) -> None:
        pass


    def _Execute(self) -> None:
        self.Execute_PRE()
        self.Execute()
        self.Execute_PST()


    def Execute_PST(self) -> None:
        self.log_environment()
        os.environ['PATH'] = self._PATH_old
        os.environ['PYTHONPATH'] = self._PYTHONPATH_old
        self.log_environment()

        self.process_wsgipy()
        self.process_updatepy()
