import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[task] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from sitetaskexecutor.Sitetask._Sitetask.Sitetask import *


class deploy_site_Sitetask(
    Sitetask
):
    @classmethod
    def from_PATHFILE_executetaskpy(cls,
        PATHFILE_executetaskpy:Path=None
    ):
        pythonanywhere_username = PATHFILE_executetaskpy.parent.parent.parent.name

        target_project = {
            'getagent': agent_Gitproject,
            'getynsbase': ynsbase_Gitproject,
            'getletters': letters_Gitproject,
            'getprojekt': projekt_Gitproject,
            'getmyrta': myrta_Gitproject,
            'getuna': una_Gitproject,
            'getrs': rs_Gitproject,
            'getrsdata': rsdata_Gitproject,
            'getsc': sc_Gitproject,
            'skfb': skfb_Gitproject,
            'getfw': fw_Gitproject,
            'getsola': sola_Gitproject,
            'getln': Ln_Gitproject,

            'ynsight': ynsight_Gitproject
        }[pythonanywhere_username]()

        result = cls(
            PATHFILE_executetaskpy=PATHFILE_executetaskpy,
            target_project=target_project
        )

        return result

    def __init__(self,
        PATHFILE_executetaskpy:Path=None,
        target_project:Gitproject=None
    ):
        Sitetask.__init__(self,
            PATHFILE_executetaskpy=PATHFILE_executetaskpy
        )
        self._target_project = target_project

        self._target_project.attach_to_task(
            task=self
        )

    def pythonanywhere_username(self) -> str:
        return self.target_project().pythonanywhere_username()

    def target_project(self) -> Gitproject:
        return self._target_project

    def PATHFILE_wsgipy(self) -> Path:
        return Path(
                '/var/www/%pythonanywhere_username%_pythonanywhere_com_wsgi.py'
                    .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            )

    def Execute(self) -> None:
        logger.info(
'''# projekt:
target_project: '%target_project%'

# pythonanywhere:
pythonanywhere_username: '%pythonanywhere_username%'
URL_pythonanywhere_site: '%URL_pythonanywhere_site%'

# github:
github_username: '%github_username%'

# paths:
PATHDIR_home_pythonanywhereusername: '%PATHDIR_home_pythonanywhereusername%'
PATHDIR_root: '%PATHDIR_root%'
PATHDIR_root_sitetask: '%PATHDIR_root_sitetask%'
PATHDIR_root_sitetask_sitetaskpackage: '%PATHDIR_root_sitetask_sitetaskpackage%'
PATHFILE_root_sitetask_sitetaskpackage_executetaskpy: '%PATHFILE_root_sitetask_sitetaskpackage_executetaskpy%'
PATHFILE_wsgipy: '%PATHFILE_wsgipy%'
PATHFILE_root_sitetask_sitetaskpackage_updatepy: '%PATHFILE_root_sitetask_sitetaskpackage_updatepy%'
PATHFILE_home_pythonanywhereusername_updatepy: '%PATHFILE_home_pythonanywhereusername_updatepy%'
'''
            .replace('%target_project%', str(self.target_project()))
            \
            .replace('%pythonanywhere_username%', self.pythonanywhere_username())
            .replace('%URL_pythonanywhere_site%', self.URL_pythonanywhere_site())
            \
            .replace('%github_username%', self.github_username())
            \
            .replace('%PATHDIR_home_pythonanywhereusername%', str(self.PATHDIR_home_pythonanywhereusername()))
            .replace('%PATHDIR_root%', str(self.PATHDIR_root()))
            .replace('%PATHDIR_root_sitetask%', str(self.PATHDIR_root_sitetask()))
            .replace('%PATHDIR_root_sitetask_sitetaskpackage%', str(self.PATHDIR_root_sitetask_sitetaskpackage()))
            .replace('%PATHFILE_root_sitetask_sitetaskpackage_executetaskpy%', str(self.PATHFILE_root_sitetask_sitetaskpackage_executetaskpy()))
            .replace('%PATHFILE_wsgipy%', str(self.PATHFILE_wsgipy()))
            .replace('%PATHFILE_root_sitetask_sitetaskpackage_updatepy%', str(self.PATHFILE_root_sitetask_sitetaskpackage_updatepy()))
            .replace('%PATHFILE_home_pythonanywhereusername_updatepy%', str(self.PATHFILE_home_pythonanywhereusername_updatepy()))
        )

        for projekt in self.projekts_all():
            projekt.uninstall_as_package()


        URL_github_projekt_repository = self.target_project().URLSSH_github_projekt_repository()

        PATHDIR_root_projektrepository = self.PATHDIR_root() / self.target_project().NAME()
        if not PATHDIR_root_projektrepository.is_dir():
            subprocess.run(
                [
                    'git',
                    'clone',
                    URL_github_projekt_repository
                ],
                cwd=str(self.PATHDIR_root())
            )

        PATHfile_root_projektrepository_makepy = PATHDIR_root_projektrepository / 'make.py'
        subprocess.run(
            [
                'python3.6',
                PATHfile_root_projektrepository_makepy
            ],
            cwd=PATHDIR_root_projektrepository
        )

        # wsgi.py:
        logger.info('Process wsgi.py...')
        logger.info(
'''PATHFILE_wsgipy=%PATHFILE_wsgipy%'''
            .replace('%PATHFILE_wsgipy%', str(self.PATHFILE_wsgipy()))
        )

        logger.info('Write wsgi.py file...')

        PATHFILE_VERSION = PATHDIR_root_projektrepository / 'VERSION'
        FCONTENT_VERSION_list = PATHFILE_VERSION.read_text().splitlines()

        ver_major = int(FCONTENT_VERSION_list[1])
        ver_minor = int(FCONTENT_VERSION_list[2])

        PATHDIR_root_out_projekt_pythonpath =\
            self.PATHDIR_root() / \
            (
'_out/Release/%NAME%-pub-%major%.%minor%-lnx/%NAME%/_projekt'
                 .replace('%NAME%', self.target_project().NAME())
                 .replace('%major%', str(ver_major))
                 .replace('%minor%', str(ver_minor))
             )

        PATHDIR_root_out_site = self.PATHDIR_root() / '_out/Release/%NAME%-pub-%major%.%minor%-lnx/site'

        wsgipy_template = \
'''import sys, os
from pathlib import Path

sys.path = [
    '%PATHDIR_root_out_projekt_pythonpath%',
    '%PATHDIR_root_out_site%'
] + sys.path

from sitepub_%NAME%.Sitepubapp import create_app

application = create_app()'''

        wsgipy_fc = wsgipy_template\
            .replace('%PATHDIR_root_out_projekt_pythonpath%', str(PATHDIR_root_out_projekt_pythonpath))\
            .replace('%PATHDIR_root_out_site%', str(PATHDIR_root_out_site))\
            .replace('%NAME%', self.target_project().NAME())

        self.PATHFILE_wsgipy().write_text(
            wsgipy_fc
        )

        logger.info('WSGIPY_FILE_BEGIN' + wsgipy_fc + 'WSGIPY_FILE_END')
        logger.info('Write wsgi.py file!')
        logger.info('Process wsgi.py!')