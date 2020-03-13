set -e
if [ -d "build/" ];then
rm -r build
fi
if [ -d "dist/" ];then
rm -r dist
fi
if [ -d "thc_upload.egg-info/" ];then
rm -r thc_upload.egg-info
fi
python setup.py bdist_wheel