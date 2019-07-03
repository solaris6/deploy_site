import os
import shutil
import subprocess
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

    site = 'site_' + project
    PATHDIR_site = PATHDIR_home_user / site

    URL_repository = '''https://github.com/solaris6/%project%.git'''\
        .replace('%project%', project)
    PATHDIR_repository = PATHDIR_home_user / project
    PATHDIR_repository_site = PATHDIR_repository / '_site' / site

    PATHFILE_wsgi_py = Path(
        '/var/www/%USER%_pythonanywhere_com_wsgi.py'
            .replace('%USER%', USER)
    )

    print('test0')
    print(sys.argv)
    print(__file__)
    print(PATHFILE_home_user_deploy_site_deploy_site_py)
    print(PATHDIR_home_user_deploy_site)
    print(PATHDIR_home_user)
    print(USER)
    print(project)
    print(site)
    print(PATHDIR_site)
    print(URL_repository)
    print(PATHDIR_repository)
    print(PATHDIR_repository_site)

    if PATHDIR_repository.is_dir():
        shutil.rmtree(PATHDIR_repository)

    subprocess.run(['git', 'clone', URL_repository])

    if PATHDIR_repository.is_dir():
        shutil.copytree(PATHDIR_repository_site, PATHDIR_site)
        shutil.rmtree(PATHDIR_repository)

    os.system('touch ' + str(PATHFILE_wsgi_py))