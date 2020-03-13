import json
import os
import re
import subprocess

import click

# 设定在最开始目录下存在一个repo_config.ini文件，用来记录每个仓库的上传链接
REPO_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'repo_config.json')
BASE_URL = 'https://cloud.tsinghua.edu.cn'
@click.command()
@click.option('--repo_name', type=click.STRING, required=True, help='the repo name in that you want to upload file')
@click.option('--file_name', type=click.Path(exists=True), required=True, help='the file name that you want to upload')
def main(repo_name, file_name):
    '''
    upload file to target repo
    '''
    # load repo list from the json file
    with open(REPO_CONFIG_FILE, 'r') as f:
        repo_config_dict = json.load(f)
    assert len(repo_config_dict.keys()) > 0, f'no repo_config in {REPO_CONFIG_FILE}'
    # test if repo name in repo_config_list
    if repo_name in repo_config_dict:
        repo_url = repo_config_dict[repo_name]
        assert type(repo_url) == str, f'the value in must be a string in {REPO_CONFIG_FILE}'
    else:
        print(f'there is no {repo_name} in {REPO_CONFIG_FILE}')
        print(f'the repo_config_list is:')
        for k, v in repo_config_dict.items():
            print(f'{k}: {v}')
        return 0
    # 当找到了对应的仓库链接，按照网上给出的方案进行测试
    # https://stackoverflow.com/questions/38742893/how-to-use-a-seafile-generated-upload-link-w-o-authentication-token-from-command
    # check for net status
    result = subprocess.check_output(['python3', '/home/sunhanbo/backup/scripts/tunet.py']).decode().split('\n')
    result = list(filter(lambda x:len(x)>0, result))
    if len(result) == 1 and 'on' in result[0]:
        net_status_is_on = True
    elif len(result) == 2 and 'off' in result[0] and '200' in result[1]:
        net_status_is_on = True
    else:
        net_status_is_on = False
    if not net_status_is_on:
        print(f'can not establish network')
        return 0
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
    abs_file_path = os.path.abspath(file_name)
    base_file_name = os.path.basename(file_name)
    # upload file
    command = f'curl {upload_url} -F file=@{abs_file_path} -F filename={base_file_name} -F parent_dir="/" -s'
    print(f'upload file using {command}')
    result = subprocess.check_output([command], shell=True).decode()
    print(result)
