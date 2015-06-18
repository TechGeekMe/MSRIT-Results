def prepare_deploy():
    local('git add . && git commit')
    local('git push')

def deploy():
    code_dir = '/var/www/html/MSRIT-Results/'
    with cd(code_dir):
        run('git pull')
        with cd(code_dir+'results'):
            run('touch wsgi.py')
        
