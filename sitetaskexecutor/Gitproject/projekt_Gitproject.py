from sitetaskexecutor.Gitproject._Gitproject.Gitproject import *

class projekt_Gitproject(
    Gitproject
):
    def NAME(self) -> str:
        return 'projekt'

    def pythonanywhere_username(self) -> str:
        return 'getprojekt'

    def project_or_workshop(self) -> str:
        return 'project'

    def github_url_type(self) -> str:
        return 'ssh'

    def is_uninstall_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return [
            'projekt',
            'projekt.sh',
            'projekt.bat',
            'projekt_.py',
            'projekt.py'
        ]
