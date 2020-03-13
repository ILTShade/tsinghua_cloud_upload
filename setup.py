import os

from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    INSTALL_REQUIRES = f.read().splitlines()

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name = "thc_upload",
    version = "0.0.1",
    author = "Hanbo Sun",
    author_email = "sun-hb17@mails.tsinghua.edu.cn",
    description = "A tool to upload file to tsinghua cloud in terminal",
    url = "https://github.com/ILTShade/tsinghua_cloud_upload",
    packages = find_packages(),
    install_requires = INSTALL_REQUIRES,
    long_description = LONG_DESCRIPTION,
    entry_points = {
        'console_scripts': [
            'thc_upload=tsinghua_cloud_upload.process:main'
        ]
    },
)
