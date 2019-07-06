import os, shutil, subprocess, sys
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('[deploy] Deploy site...')

    PATHFILE_home_user_root_deploysite_deploypy = Path(sys.argv[0])
    PATHDIR_home_user_root_deploysite = PATHFILE_home_user_root_deploysite_deploypy.parent
    PATHDIR_home_user_root = PATHDIR_home_user_root_deploysite.parent
    PATHDIR_home_user = PATHDIR_home_user_root.parent

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
    URL_projectrepository = '''https://github.com/solaris6/%project%.git'''\
        .replace('%project%', project)

    PATHDIR_root_sitepackage = PATHDIR_home_user_root / sitepackage

    PATHDIR_root_repositories = PATHDIR_home_user_root / 'repositories'
    PATHDIR_root_repositories_projectrepository = PATHDIR_root_repositories / project
    PATHDIR_root_repositories_projectrepository_sitepackage = PATHDIR_root_repositories_projectrepository / '_site' / sitepackage

    PATHFILE_wsgi_py = Path(
        '/var/www/%USER%_pythonanywhere_com_wsgi.py'
            .replace('%USER%', USER)
    )

    logger.info(
'''sys.argv=%sys.argv%
__file__=%__file__%
PATHFILE_home_user_root_deploysite_deploypy=%PATHFILE_home_user_root_deploysite_deploypy%
PATHDIR_home_user_root_deploysite=%PATHDIR_home_user_root_deploysite%
PATHDIR_home_user_root=%PATHDIR_home_user_root%
PATHDIR_home_user=%PATHDIR_home_user%

USER=%USER%
project=%project%
sitepackage=%sitepackage%
URL_site=%URL_site%
URL_projectrepository=%URL_projectrepository%

PATHDIR_root_sitepackage=%PATHDIR_root_sitepackage%

PATHDIR_root_repositories=%PATHDIR_root_repositories%
PATHDIR_root_repositories_projectrepository=%PATHDIR_root_repositories_projectrepository%
PATHDIR_root_repositories_projectrepository_sitepackage=%PATHDIR_root_repositories_projectrepository_sitepackage%

PATHFILE_wsgi_py=%PATHFILE_wsgi_py%'''
        .replace('%sys.argv%', str(sys.argv))
        .replace('%__file__%', str(__file__))
        .replace('%PATHFILE_home_user_root_deploysite_deploypy%', str(PATHFILE_home_user_root_deploysite_deploypy))
        .replace('%PATHDIR_home_user_root_deploysite%', str(PATHDIR_home_user_root_deploysite))
        .replace('%PATHDIR_home_user_root%', str(PATHDIR_home_user_root))
        .replace('%PATHDIR_home_user%', str(PATHDIR_home_user))
        \
        .replace('%USER%', str(USER))
        .replace('%project%', str(project))
        .replace('%sitepackage%', str(sitepackage))
        .replace('%URL_site%', str(URL_site))
        .replace('%URL_projectrepository%', str(URL_projectrepository))
        \
        .replace('%PATHDIR_root_sitepackage%', str(PATHDIR_root_sitepackage))
        \
        .replace('%PATHDIR_root_repositories%', str(PATHDIR_root_repositories))
        .replace('%PATHDIR_root_repositories_projectrepository%', str(PATHDIR_root_repositories_projectrepository))
        .replace('%PATHDIR_root_repositories_projectrepository_sitepackage%', str(PATHDIR_root_repositories_projectrepository_sitepackage))
        \
        .replace('%PATHFILE_wsgi_py%', str(PATHFILE_wsgi_py))
    )


    PATHDIR_root_repositories.mkdir(parents=True)


    logger.info('[deploy] Setup project dependencies...')

    logger.info('[deploy] Setup project dependencies!')


    logger.info('[deploy] Downloading project repository...')
    subprocess.run(['git', 'clone', URL_projectrepository], cwd=str(PATHDIR_root_repositories))
    logger.info('[deploy] Downloading project repository!')

    logger.info('[deploy] Install project site...')
    if PATHDIR_root_sitepackage.is_dir():
        shutil.rmtree(PATHDIR_root_sitepackage)

    if PATHDIR_root_repositories_projectrepository.is_dir():
        shutil.copytree(PATHDIR_root_repositories_projectrepository_sitepackage, PATHDIR_root_sitepackage)
    logger.info('[deploy] Install project site!')

    logger.info('[deploy] Touch wsgi.py...')
    os.system('touch ' + str(PATHFILE_wsgi_py))
    logger.info('[deploy] Touch wsgi.py!')

    logger.info('[deploy] Deploy site!')
