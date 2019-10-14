from pathlib import Path
from typing import List

from sitedeployer.Projekt.Workshop._Workshop.Workshop import Workshop


class ynsight_Workshop(
    Workshop
):
    def NAME(self) -> str:
        return 'ynsight'

    def pythonanywhere_username(self) -> str:
        return 'ynsight'

    def github_url_type(self) -> str:
        return 'ssh'

    def version_list(self) -> List[int]:
        return [2019, 2, 0]

    def is_uninstall_as_package_supported(self) -> bool:
        return False

    def package_executables(self) -> List[str]:
        return None


    def PATHDIRS_packages_to_upload_on_testpypi(self) -> List[Path]:
        return []