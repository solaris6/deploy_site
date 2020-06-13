from sitetaskexecutor.Gitproject._Gitproject.Gitproject import *

class sc_Gitproject(
    Gitproject
):
    def NAME(self) -> str:
        return 'sc'
    
    def pythonanywhere_username(self) -> str:
        return 'getsc'

    def project_or_workshop(self) -> str:
        return 'project'

    def github_url_type(self) -> str:
        return 'ssh'

    def is_uninstall_as_package_supported(self) -> bool:
        return False

    def package_executables(self) -> List[str]:
        return []
