from tsinghua_cloud_upload import process

# test for some initial setting, upload this file to DPU
process.main(['--repo_name', 'DPU', '--file_name', f'{__file__}'])