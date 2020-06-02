import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[deployer] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


from sitedeployer.Task._Task.Task import *



class upload_on_pypi_Task(
    Task
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
        Task.__init__(self,
            PATHFILE_deploypy=PATHFILE_deploypy
        )

    def pythonanywhere_username(self) -> str:
        return 'ynsbuilder'


    def Execute(self) -> None:
        for projekt in self.projekts_all():
            projekt.upload_on_pypi()
