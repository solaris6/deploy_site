import shutil, subprocess, sys
from pathlib import Path

import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[update] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


if __name__ == '__main__':
    logger.info('Updating sitedeployer package (then use them to deploy_site or upload_on_pypi Tasks)...')


    PATHFILE_updatepy = Path(sys.argv[0])
    PATHDIR_root = PATHFILE_updatepy.parent / 'root'
    PATHDIR_root_sitedeployer = PATHDIR_root / 'sitedeployer'
    PATHFILE_root_sitedeployer_executetaskpy = PATHDIR_root_sitedeployer / 'execute_task.py'


    logger.info(
'''PATHFILE_updatepy=%PATHFILE_updatepy%
PATHDIR_root=%PATHDIR_root%
PATHDIR_root_sitedeployer=%PATHDIR_root_sitedeployer%
PATHFILE_root_sitedeployer_executetaskpy=%PATHFILE_root_sitedeployer_executetaskpy%'''
          .replace('%PATHFILE_updatepy%', str(PATHFILE_updatepy))
          .replace('%PATHDIR_root%', str(PATHDIR_root))
          .replace('%PATHDIR_root_sitedeployer%', str(PATHDIR_root_sitedeployer))
          .replace('%PATHFILE_root_sitedeployer_executetaskpy%', str(PATHFILE_root_sitedeployer_executetaskpy))
    )


    logger.info('Creating root dir...')
    if PATHDIR_root.is_dir():
        shutil.rmtree(PATHDIR_root)
    PATHDIR_root.mkdir()
    logger.info('Created root dir!')


    logger.info('Updating sitedeployer package...')
    subprocess.run(
        ['git', 'clone', 'https://github.com/ynsight/sitedeployer.git'],
        cwd=str(PATHDIR_root)
    )
    logger.info('Updated sitedeployer package!')


    logger.info('Using sitedeployer package...')
    subprocess.run(
        ['python3.6', PATHFILE_root_sitedeployer_executetaskpy]
    )
    logger.info('Used sitedeployer package!')


    logger.info('Updated sitedeployer package (then used them to deploy_site or upload_projects_on_pypi)!')
