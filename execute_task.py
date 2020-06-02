import shutil
import sys
from pathlib import Path

sys.path.append(str(Path(sys.argv[0]).parent))

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from sitedeployer.Task.deploy_site_Task import deploy_site_Task
from sitedeployer.Task.upload_on_pypi_Task import upload_on_pypi_Task


if __name__ == '__main__':
    PATHFILE_home_pythonanywhereusername_root_sitedeployer_executetaskpy = Path(sys.argv[0])
    PATHDIR_home_pythonanywhereusername_root_sitedeployer = PATHFILE_home_pythonanywhereusername_root_sitedeployer_executetaskpy.parent
    PATHDIR_home_pythonanywhereusername_root = PATHDIR_home_pythonanywhereusername_root_sitedeployer.parent
    PATHDIR_home_pythonanywhereusername = PATHDIR_home_pythonanywhereusername_root.parent
    pythonanywhere_username = PATHDIR_home_pythonanywhereusername.name

    if pythonanywhere_username == 'ynsbuilder':
        deploy_site_Task.from_PATHFILE_deploypy(
            PATHFILE_deploypy=PATHFILE_home_pythonanywhereusername_root_sitedeployer_executetaskpy
        )._Execute()

    else:
        upload_on_pypi_Task.from_PATHFILE_deploypy(
            PATHFILE_deploypy=PATHFILE_home_pythonanywhereusername_root_sitedeployer_executetaskpy
        )._Execute()


    # update.py:
    logger.info('Writing update.py file...')

    FILENAME_updatepy = 'update.py'
    PATHFILE_home_pythonanywhereusername_root_sitedeployer_updatepy = PATHDIR_home_pythonanywhereusername_root_sitedeployer / FILENAME_updatepy
    PATHFILE_home_pythonanywhereusername_updatepy = PATHDIR_home_pythonanywhereusername / FILENAME_updatepy


    logger.info(
'''update.py paths:
PATHFILE_home_pythonanywhereusername_root_sitedeployer_updatepy=%PATHFILE_home_pythonanywhereusername_root_sitedeployer_updatepy%
PATHFILE_home_pythonanywhereusername_updatepy=%PATHFILE_home_pythonanywhereusername_updatepy%'''
        .replace('%PATHFILE_home_pythonanywhereusername_root_sitedeployer_updatepy%', str(PATHFILE_home_pythonanywhereusername_root_sitedeployer_updatepy))
        .replace('%PATHFILE_home_pythonanywhereusername_updatepy%', str(PATHFILE_home_pythonanywhereusername_updatepy))
    )

    shutil.copyfile(
        PATHFILE_home_pythonanywhereusername_root_sitedeployer_updatepy,
        PATHFILE_home_pythonanywhereusername_updatepy
    )
    logger.info('Writed update.py file!')