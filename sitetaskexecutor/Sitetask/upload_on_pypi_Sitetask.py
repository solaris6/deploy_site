import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("[task] - %(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


from sitetaskexecutor.Sitetask._Sitetask.Sitetask import *



class upload_on_pypi_Sitetask(
    Sitetask
):
    @classmethod
    def from_PATHFILE_executetaskpy(cls,
        PATHFILE_executetaskpy:Path=None
    ):
        result = cls(
            PATHFILE_executetaskpy=PATHFILE_executetaskpy
        )
        return result

    def __init__(self,
        PATHFILE_executetaskpy:Path=None
    ):
        Sitetask.__init__(self,
            PATHFILE_executetaskpy=PATHFILE_executetaskpy
        )

    def pythonanywhere_username(self) -> str:
        return 'ynsbuilder'


    def Execute(self) -> None:
        for projekt in self.projekts_all():
            projekt.upload_on_pypi()
