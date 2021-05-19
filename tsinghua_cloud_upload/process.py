import json
import os
import re
import subprocess

import click

def check_or_init_config_and_load(config_path):
    # check repo config path
    if not os.path.exists(config_path):
        os.mkdir(config_path)
        print(f'mkdir {config_path} for saving config file')
    config_file = os.path.join(config_path, 'repo_config.json')
    if not os.path.exists(config_file):
        open(config_file, 'w').close()
        print(f'generate empty file {config_file} for saving config file')
    # load repo list from the json file
    with open(config_file, 'r') as f:
        try:
            repo_config_dict = json.load(f)
        except:
            repo_config_dict = dict()
    return repo_config_dict

def write_config(config_path, repo_config_dict):
    config_file = os.path.join(config_path, 'repo_config.json')
    with open(config_file, 'w') as f:
        json.dump(repo_config_dict, f)

def check_network():
    import requests
    try:
        html = requests.get('http://www.baidu.com', timeout=2)
    except:
        return False
    return True

# assert len(repo_config_dict.keys()) > 0, f'no repo_config in {REPO_CONFIG_FILE}'
# 设定在最开始目录下存在一个repo_config.ini文件，用来记录每个仓库的上传链接
REPO_CONFIG_PATH = os.path.join(os.environ['HOME'], '.thc_upload')
BASE_URL = 'https://cloud.tsinghua.edu.cn'
@click.command()
@click.option('--mode', type=click.Choice(['set', 'upload']), required=True, help='"set" for set upload url for repo name, "upload" for upload')
@click.option('--repo_name', type=click.STRING, required=True, help='the repo name in that you want to upload file')
@click.option('--operate_name', type=click.STRING, required=True, help='the operate name that you want to set (url) or upload (file)')
def main(mode, repo_name, operate_name):
    '''
    set url or upload file for repo name
    '''
    repo_config_dict = check_or_init_config_and_load(REPO_CONFIG_PATH)
    if mode == 'set':
        # set
        repo_config_dict[repo_name] = operate_name
        # write
        write_config(REPO_CONFIG_PATH, repo_config_dict)
        print(f'set {operate_name} for {repo_name}')
    if mode == 'upload':
        # check network
        if not check_network():
            raise Exception(f'can not establish network')
        # test if repo name in repo_config_dict
        if repo_name in repo_config_dict:
            repo_url = repo_config_dict[repo_name]
        else:
            print(f'the repo_config_dict is:')
            for k, v in repo_config_dict.items():
                print(f'{k}: {v}')
            raise Exception(f'however, {repo_name} DOES NOT in repo_config_dict')
        # 查找返回的链接
        result = subprocess.check_output(['curl', repo_url, '-s']).decode().split('\n')
        result = list(filter(lambda x:('ajax/u/d' in x), result))
        assert len(result) == 1, f'something error happend in curl {repo_url}'
        res = re.search("^\s*url: '(?P<url>.+)',$", result[0])
        intermediate_url = res.groupdict()['url']
        SUFFIX = "-H 'Accept: application/json' -H 'X-Requested-With: XMLHttpRequest'"
        # get upload url
        command = f'curl {BASE_URL}{intermediate_url} {SUFFIX} -s'
        print(f'get upload url using {command}')
        result = subprocess.check_output([command], shell=True).decode().split('\n')[0]
        upload_url = json.loads(result)['url']
        # get absolute path for upload
        abs_file_path = os.path.abspath(operate_name)
        base_file_name = os.path.basename(operate_name)
        # upload file
        command = f'curl {upload_url} -F file=@{abs_file_path} -F filename={base_file_name} -F parent_dir="/"'
        print(f'upload file using {command}')
        result = subprocess.check_output([command], shell=True).decode()
        print(result)
