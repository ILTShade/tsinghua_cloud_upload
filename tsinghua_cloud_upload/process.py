import os

import click
import json


# 设定在最开始目录下存在一个repo_config.ini文件，用来记录每个仓库的上传链接
REPO_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'repo_config.json')
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
    # get absolute path for upload
    abs_file_path = os.path.abspath(file_name)