from sitetaskexecutor.Gitproject._Gitproject.Gitproject import *


class fw_Gitproject(
    Gitproject
):
    def NAME(self) -> str:
        return 'fw'
    
    def pythonanywhere_username(self) -> str:
        return 'getfw'

    def project_or_workshop(self) -> str:
        return 'project'

    def github_url_type(self) -> str:
        return 'ssh'

    def is_uninstall_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return [
            'fw',
            'fw.sh',
            'fw.bat',
            'fw_.py',
            'fw.py'
        ]
