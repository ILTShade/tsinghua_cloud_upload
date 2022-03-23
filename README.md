# TsinghuaCloudUpload

a script for upload file to tsinghua cloud.

## Install

```shell
cd workspace_folder/
pip install -e .
```

## Usereg

First, you can use "set" mode to set the repo upload link to a user-defined name, like
```shell
thc_upload --mode set --repo_name somename_you_like --operate_name THE_TSINGHUA_REPO_UPLOAD_LINK
```
And then, you can use "somename_you_like" to upload file in server, like
```shell
thc_upload --mode upload --repo_name somename_you_like --operate_name THE_FILE_NAME
```
PLEASE check in the upload command, the link of the specificed repo_name, you must have already set



```text
Usage: thc_upload [OPTIONS]

  set url or upload file for repo name

Options:
  --mode [set|upload]  "set" for set upload url for repo name, "upload" for upload  [required]
  --repo_name TEXT     the repo name in that you want to upload file [required]
  --operate_name TEXT  the operate name that you want to set (url) or upload (file)  [required]
  --help               Show this message and exit.
```
