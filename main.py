import sys
from pathlib import Path

if __name__ == '__main__':

    PATHFILE_home_user_deploy_site_deploy_site_py = Path(sys.argv[0])
    PATHDIR_home_user_deploy_site = PATHFILE_home_user_deploy_site_deploy_site_py.parent
    PATHDIR_home_user = PATHDIR_home_user_deploy_site.parent
    USER = PATHDIR_home_user.name
    project = {
        'getsola': 'sola',
        'getbase': 'base',
        'getmyrta': 'myrta',
        'getuna': 'una',
        'getrs': 'rs',
        'getfw': 'fw',
        'getln': 'Ln',
        'ynsight': 'ynsight'
    }[USER]

    site_project = 'site_' + project
    PATHDIR_site_project = PATHDIR_home_user / site_project

    URL_project_repository = '''https://github.com/solaris6/%project%.git'''\
        .replace('%project%', project)
    PATHDIR_project_repository = PATHDIR_home_user / project

    print('test0')
    print(sys.argv)
    print(__file__)
    print(PATHFILE_home_user_deploy_site_deploy_site_py)
    print(PATHDIR_home_user_deploy_site)
    print(PATHDIR_home_user)
    print(USER)
    print(project)
    print(site_project)
    print(PATHDIR_site_project)
    print(URL_project_repository)
    print(PATHDIR_project_repository)