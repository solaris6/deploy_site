import logging

from sitedeployer.utils import log_environment

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from sitedeployer._Sitetask.Sitetask import *



class Builder(
    Sitetask
):
    @classmethod
    def from_PATHFILE_deploypy(cls,
        PATHFILE_deploypy:Path=None
    ):
        result = cls(
            PATHFILE_deploypy=PATHFILE_deploypy
        )
        return result

    def __init__(self,
        PATHFILE_deploypy:Path=None
    ):
        Sitetask.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def pythonanywhere_username(self) -> str:
        return 'ynsbuilder'

    def Build(self) -> None:
        log_environment(logger=logger)
        logger.info('Build and Upload projects...')

        for projekt in self.projekts_all():
            if projekt.NAME() == 'ynsbase':
                projekt.upload_on_pypi()

        logger.info('Builded and Uploaded projects!')
