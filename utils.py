import subprocess
import os

def get_envs():
    output = subprocess.check_output('conda env list', universal_newlines=True,shell=True)
    env = []
    lines = output.split('\n')
    lines = lines[2:]
    for line in lines:
        env.append(line.split(' ')[0])
    return envs

def save_env(env):
    subprocess.run(f"conda env export --name {env}> {env}.txt",shell=True)
    assert os.path.exists('{}.txt'.format(env))

def init_local_repo(url):
    subprocess.run(f'git clone {url}',shell=True)
    repo_name = url.split('/')[-1].split('.')[0]
    assert os.path.exists(repo_name)

def remove_env(env):
    subprocess.run(f"conda remove --name {env} --all")
    envs = get_envs()
    assert env not in envs
    


