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

from sitedeployer.Builder import Builder
from sitedeployer.Deployer import Deployer

if __name__ == '__main__':
    logger.info('Deploy site...')
    PATHFILE_deploypy = Path(sys.argv[0])
    pythonanywhere_username = PATHFILE_deploypy.parent.parent.parent.name

    if pythonanywhere_username == 'ynsbuilder':
        Builder.from_PATHFILE_deploypy(
            PATHFILE_deploypy=PATHFILE_deploypy
        ).Build()

    else:
        Deployer.from_PATHFILE_deploypy(
            PATHFILE_deploypy=PATHFILE_deploypy
        ).Deploy()

    logger.info('Deploy site!')
