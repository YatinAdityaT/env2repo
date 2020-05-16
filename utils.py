import os
import pickle
import subprocess

def init_local_repo(url):
    print('cloning :',url)
    subprocess.run(f'git clone {url} repos/{get_repo_name_from_url(url)}',shell=True)
    repo_name = url.split('/')[-1].split('.')[0]
    assert os.path.exists(os.path.join('repos',repo_name))
    return repo_name

def get_repo_name_from_url(url):
    return url.split('/')[-1].split('.')[0]

def pull_remote():
    subprocess.run(f'git pull',shell=True)

def get_envs():
    output = subprocess.check_output('conda env list', universal_newlines=True,shell=True)
    envs = []
    lines = output.split('\n')
    lines = lines[2:]
    for line in lines:
        env = line.split(' ')[0]
        if not env == '':
            envs.append(env)
    return envs

def save_env(env,repo_name,path):
    path_to_env = os.path.join(path,env)
    if not os.path.exists(path_to_env):
        version = '0'
        os.makedirs(path_to_env)
    else:
        version = get_latest_version_number(path_to_env)

    path_to_env_version = os.path.join(path_to_env,version)
    os.mkdir(path_to_env_version)

    file_path = os.path.join(path_to_env_version,env+'.yml')
    subprocess.run(f"conda env export --name {env} > {file_path}",shell=True)
    assert os.path.exists(file_path)

    file_path_from_history = os.path.join(path_to_env_version,env+'_from_history.yml')
    subprocess.run(f"conda env export --from-history --name {env} > {file_path_from_history}",shell=True)
    assert os.path.exists(file_path_from_history)

    if version == '0':
        update_github(env,repo_name,path_to_env,"add new env")
    else:
        update_github(env,repo_name,path_to_env,"add version",version=version)
    return version

def remove_env(env):
    subprocess.run(f"conda remove --name {env} --all",shell=True)
    envs = get_envs()
    assert env not in envs

def envs_in_repo(repo_name):
    return os.listdir(os.path.join('repos',repo_name))

def list_of_repos():
    return os.listdir('repos')

def update_session_file(saved_session):
    pickle_out = open("saved_session.pickle",'wb')
    pickle.dump(saved_session, pickle_out)
    pickle_out.close()

def get_latest_version_number(path_to_env):
    list_of_versions = os.listdir(path_to_env)
    print(list_of_versions)
    if len(list_of_versions) == 0:
        return 0
    else:
        return str(max(list(map(int,list_of_versions))) + 1)

def save_env_temp(env):
    subprocess.run(f"conda env export --name {env} > temp.yml",shell=True)
    assert os.path.exists('temp.yml')

    file_path_from_history = 'temp_from_history.yml'
    subprocess.run(f"conda env export --from-history --name {env} > {file_path_from_history}",shell=True)
    assert os.path.exists(file_path_from_history)

def check_prev_backup(path_to_env,env):
    if not os.path.exists(path_to_env):
        return False
    latest_version = str(int(get_latest_version_number(path_to_env)) - 1)
    path_to_yml_file = os.path.join(path_to_env,latest_version,env+'.yml')
    save_env_temp(env)

    with open(path_to_yml_file) as f1:
        with open('temp.yml') as f2:
            if f1.read() == f2.read():
                return True
            else:
                return False

def update_github(env,repo_name,path_to_env,action,version=None):
    workingdir = os.getcwd()
    os.chdir(os.path.join('repos',repo_name))
    if action=="add version":
        path_to_env_version = os.path.join(env,version)
        subprocess.run(f"git add {path_to_env_version}",shell=True)
        subprocess.run(f'git commit -m "add {env} version {version}"',shell=True)
        subprocess.run(f'git push',shell=True)

    elif action=="remove env backup":
        subprocess.run(f"git add {env}",shell=True)
        subprocess.run(f'git commit -m "removed {env}"',shell=True)
        subprocess.run(f'git push',shell=True)

    elif action=="add new env":
        subprocess.run(f"git add {env}",shell=True)
        subprocess.run(f'git commit -m "add {env} version 0"',shell=True)
        subprocess.run(f'git push',shell=True)

    os.chdir(workingdir)