import json
import os
from typing import Dict, Any


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
