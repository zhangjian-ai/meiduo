#!/bin/bash

echo "=============前端打包============="
cd meiduo_mall_frontend
npm run build
cd ..
echo "=============打包完成============="
echo "=============提交代码============="
git add .
git commit -m "update new version"
git push origin master
echo "=============提交完成============="
#echo "=============构建任务============="
#python3 jenkins_release.py









