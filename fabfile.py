def prepare_deploy:
    local('git add . && git commit')
    local('git push')
    
