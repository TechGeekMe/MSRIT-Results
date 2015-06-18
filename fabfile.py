from fabric.api import local, settings, abort, run, cd

def prepare_deploy(message):
    local('git add . && git commit'+" -m '"+message+"'")
    local('git push')

def deploy():
    code_dir = '/var/www/html/MSRIT-Results/'
    with cd(code_dir):
        run('git pull')
        with cd(code_dir+'results'):
            run('touch wsgi.py')
        
        
