import os
import shutil
import subprocess
import sys
from pathlib import Path

if __name__ == '__main__':
    print('[deploy] Deploy site...')
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
        'ynsight': 'ynsight',
        'getprojekt': 'project'
    }[USER]

    sitepackage = 'site_' + project
    URL_site = USER + '.pythonanywhere.com'
    PATHDIR_sitepackage = PATHDIR_home_user / sitepackage

    URL_projectrepository = '''https://github.com/solaris6/%project%.git'''\
        .replace('%project%', project)

    PATHDIR_repositories = PATHDIR_home_user / 'repositories'
    PATHDIR_projectrepository = PATHDIR_repositories / project
    PATHDIR_projectrepository_sitepackage = PATHDIR_projectrepository / '_site' / sitepackage

    PATHFILE_wsgi_py = Path(
        '/var/www/%USER%_pythonanywhere_com_wsgi.py'
            .replace('%USER%', USER)
    )

    print(
'''sys.argv=%sys.argv%
__file__=%__file__%
PATHFILE_home_user_deploy_site_deploy_site_py=%PATHFILE_home_user_deploy_site_deploy_site_py%
PATHDIR_home_user_deploy_site=%PATHDIR_home_user_deploy_site%
PATHDIR_home_user=%PATHDIR_home_user%
USER=%USER%
project=%project%
sitepackage=%sitepackage%
URL_site=%URL_site%
PATHDIR_sitepackage=%PATHDIR_sitepackage%
URL_projectrepository=%URL_projectrepository%
PATHDIR_repositories=%PATHDIR_repositories%
PATHDIR_projectrepository=%PATHDIR_projectrepository%
PATHDIR_projectrepository_sitepackage=%PATHDIR_projectrepository_sitepackage%
PATHFILE_wsgi_py=%PATHFILE_wsgi_py%'''
        .replace('%sys.argv%', str(sys.argv))
        .replace('%__file__%', str(__file__))
        .replace('%PATHFILE_home_user_deploy_site_deploy_site_py%', str(PATHFILE_home_user_deploy_site_deploy_site_py))
        .replace('%PATHDIR_home_user_deploy_site%', str(PATHDIR_home_user_deploy_site))
        .replace('%PATHDIR_home_user%', str(PATHDIR_home_user))
        .replace('%USER%', str(USER))
        .replace('%project%', str(project))
        .replace('%sitepackage%', str(sitepackage))
        .replace('%URL_site%', str(URL_site))
        .replace('%PATHDIR_sitepackage%', str(PATHDIR_sitepackage))
        .replace('%URL_projectrepository%', str(URL_projectrepository))
        .replace('%PATHDIR_repositories%', str(PATHDIR_repositories))
        .replace('%PATHDIR_projectrepository%', str(PATHDIR_projectrepository))
        .replace('%PATHDIR_projectrepository_sitepackage%', str(PATHDIR_projectrepository_sitepackage))
        .replace('%PATHFILE_wsgi_py%', str(PATHFILE_wsgi_py))
    )


    if PATHDIR_repositories.is_dir():
        shutil.rmtree(PATHDIR_repositories)
    PATHDIR_repositories.mkdir(parents=True)


    print('[deploy] Setup project dependencies...')

    print('[deploy] Setup project dependencies!')


    print('[deploy] Downloading project repository...')
    subprocess.run(['git', 'clone', URL_projectrepository, str(PATHDIR_repositories)])
    print('[deploy] Downloading project repository!')

    print('[deploy] Install project site...')
    if PATHDIR_sitepackage.is_dir():
        shutil.rmtree(PATHDIR_sitepackage)

    if PATHDIR_projectrepository.is_dir():
        shutil.copytree(PATHDIR_projectrepository_sitepackage, PATHDIR_sitepackage)
    print('[deploy] Install project site!')

    print('[deploy] Touch wsgi.py...')
    os.system('touch ' + str(PATHFILE_wsgi_py))
    print('[deploy] Touch wsgi.py!')

    print('[deploy] Deploy site!')
