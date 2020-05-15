import os
import subprocess

def init_local_repo(url):
    subprocess.run(f'git clone {url}',shell=True)
    repo_name = url.split('/')[-1].split('.')[0]
    assert os.path.exists(repo_name)
    return repo_name

def pull_remote():
    subprocess.run(f'git pull',shell=True)

def get_envs():
    output = subprocess.check_output('conda env list', universal_newlines=True,shell=True)
    env = []
    lines = output.split('\n')
    lines = lines[2:]
    for line in lines:
        env.append(line.split(' ')[0])
    return envs

def save_env(env,path):
    file_path = os.path.join(path,f'{env}.txt')
    subprocess.run(f"conda env export --from-history --name {env} > {file_path}",shell=True)
    assert os.path.exists('{}.txt'.format(env))

def remove_env(env):
    subprocess.run(f"conda remove --name {env} --all",shell=True)
    envs = get_envs()
    assert env not in envs

def push_env_to_github(env,path):
    file_path = os.path.join(path,f'{env}.txt')
    subprocess.run(f"git add {file_path}",shell=True)
    subprocess.run(f'git commit -m "add {env}"',shell=True)
    subprocess.run(f'git push',shell=True)