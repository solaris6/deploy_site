import json
import os
from typing import Dict, Any, List


def environment_report() -> Dict[str,Any]:
    result = {}
    result['cwd'] = os.getcwd()
    # result['env_vars'] = dict(os.environ)
    result['PATH'] = os.environ['PATH'].split(os.pathsep) if 'PATH' in os.environ else []
    result['PYTHONPATH'] = os.environ['PYTHONPATH'].split(os.pathsep) if 'PYTHONPATH' in os.environ else []
    return result

def log_environment(
    logger=None
) -> None:
    logger.info(
        json.dumps({
            'environment_report': environment_report()
            }, indent=2
        )
    )

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