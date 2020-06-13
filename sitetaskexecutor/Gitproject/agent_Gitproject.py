from sitetaskexecutor.Gitproject._Gitproject.Gitproject import *


class agent_Gitproject(
    Gitproject
):
    def NAME(self) -> str:
        return 'agent'
    
    def pythonanywhere_username(self) -> str:
        return 'getagent'

    def project_or_workshop(self) -> str:
        return 'project'

    def github_url_type(self) -> str:
        return 'ssh'

    def is_uninstall_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return [
            'agent',
            'agent.sh',
            'agent.bat',
            'agent_.py',
            'agent.py'
        ]
