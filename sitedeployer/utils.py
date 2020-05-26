import json
import os
import platform
from typing import Dict, Any, List

def log_environment(
    logger=None
) -> None:
    environment_report_dict = {}

    environment_report_dict['cwd'] = os.getcwd()

    if 'PATH' in os.environ:
        environment_report_dict['PATH'] = os.environ['PATH'].split(os.pathsep)
    else:
        environment_report_dict['PATH'] = []

    if 'PYTHONPATH' in os.environ:
        environment_report_dict['PYTHONPATH'] = os.environ['PYTHONPATH'].split(os.pathsep)
    else:
        environment_report_dict['PYTHONPATH'] = []

    logger.info(
        json.dumps(
            {
                'environment_report': environment_report_dict
            },
            indent=2
        )
    )

def lnx_mac_win() -> str:
    """"""
    system = platform.system()
    result = None
    if   system == 'Linux':
        result = 'lnx'
    elif system == 'Darwin':
        result = 'mac'
    elif system == 'Windows':
        result = 'win'
    return result

def remove_duplicates(
    input_list:List=None
) -> List:
    """"""
    unique_list = []

    for input_elem in input_list:
        elem_already_exists = False
        for unique_elem in unique_list:
            if unique_elem == input_elem:
                elem_already_exists = True
        if not elem_already_exists:
            unique_list.append(input_elem)

    return unique_list