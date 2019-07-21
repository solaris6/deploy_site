import shutil, subprocess, sys
from pathlib import Path
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info('[updater] Update sitedeployer package, then use them to update site...')

    PATHFILE_updatepy = Path(sys.argv[0])
    PATHDIR_root = PATHFILE_updatepy.parent / 'root'
    PATHDIR_root_sitedeployer = PATHDIR_root / '_sitedeployer'
    PATHDIR_root_sitedeployer_sitedeployerpackage = PATHDIR_root_sitedeployer / 'sitedeployer'
    PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy = PATHDIR_root_sitedeployer_sitedeployerpackage / 'deploy.py'

    logger.info(
'''PATHFILE_updatepy=%PATHFILE_updatepy%
PATHDIR_root=%PATHDIR_root%
PATHDIR_root_sitedeployer=%PATHDIR_root_sitedeployer%
PATHDIR_root_sitedeployer_sitedeployerpackage=%PATHDIR_root_sitedeployer_sitedeployerpackage%
PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy=%PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy%'''
          .replace('%PATHFILE_updatepy%', str(PATHFILE_updatepy))
          .replace('%PATHDIR_root%', str(PATHDIR_root))
          .replace('%PATHDIR_root_sitedeployer%', str(PATHDIR_root_sitedeployer))
          .replace('%PATHDIR_root_sitedeployer_sitedeployerpackage%', str(PATHDIR_root_sitedeployer_sitedeployerpackage))
          .replace('%PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy%', str(PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy))
    )

    logger.info('[updater] Create root dir...')
    if PATHDIR_root.is_dir():
        shutil.rmtree(PATHDIR_root)
    PATHDIR_root.mkdir()
    logger.info('[updater] Create root dir!')

    logger.info('[updater] Update sitedeployerpackage...')
    PATHDIR_root_sitedeployer.mkdir()
    subprocess.run(
        ['git', 'clone', 'https://github.com/solaris6/sitedeployer.git'],
        cwd=str(PATHDIR_root_sitedeployer)
    )
    logger.info('[updater] Update sitedeployerpackage!')

    logger.info('[updater] Use sitedeployerpackage...')
    subprocess.run(
        ['python3.6', PATHFILE_root_sitedeployer_sitedeployerpackage_deploypy]
    )
    logger.info('[updater] Use sitedeployerpackage!')

    logger.info('[updater] Update sitedeployer package then use them to update site!')
