from fabric.context_managers import settings, cd
from fabric.api import task, env
from fabric.operations import run
from fabric.contrib.files import exists

PROJ_ROOT = '/var/coauthor.org'
REPO_URL = "git://github.com/davidascher/coauthor.git"
DJANGO_REPO = "/var/repositories/django"

def run_manage_cmd(cmd):
    with cd('%s/coathor_site' % PROJ_ROOT):
        run('python manage.py %s' % cmd)

@task
def clone():
    run('git clone %s %s' % (REPO_URL, PROJ_ROOT))
    with cd(PROJ_ROOT):
        run('git submodule init')
        run('git config submodule.vendor/django.url %s' % DJANGO_REPO)
        run('git submodule update')

@task
def update():
    with cd(PROJ_ROOT):
        run('git pull')

@task
def deploy():
    if exists(PROJ_ROOT):
        update()
    else:
        clone()
    run_manage_cmd('collectstatic --noinput')
    run_manage_cmd('test')
    run('touch %s/wsgi/coauthor.wsgi' % PROJ_ROOT)
