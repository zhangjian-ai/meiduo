#!/bin/bash

echo "=============开始打包============="
cd student-web
npm run build
cd ..
echo "=============打包完成============="
echo "=============开始上传============="
git add StudentV4BE student-web/dist student-web/Dockerfile student-web/nginx.conf Jenkinsfile
git commit -m "update new version"
git push origin dev
echo "=============上传完成============="


