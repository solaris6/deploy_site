import os
import shutil
import subprocess
from pathlib import Path
from typing import Type, List

from sitedeployer.projects.core.Project import Project
from sitedeployer.projects.core.Projekt import Projekt, logger
from sitedeployer.utils import log_environment


class Workshop(
    Projekt
):
    def __init__(self):
        Projekt.__init__(self)


    def Init(self) -> None:
        Projekt.Init(self)
        logger.info('Init Workshop...')
        logger.info(
'''PATHDIR_root_out_type_NAME_ver_output_os_ins_lib: '%PATHDIR_root_out_type_NAME_ver_output_os_ins_lib%'
'''
            .replace('', '')
        )
        logger.info('Init Workshop!')


    # names:
    def projekt(self) -> str:
        return 'workshop'
