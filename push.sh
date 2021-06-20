#!/bin/bash

echo "=============开始打包============="
cd meiduo_mall_frontend
npm run build
cd ..
echo "=============打包完成============="
echo "=============开始上传============="
git add .
git commit -m "update new version"
git push origin master
echo "=============上传完成============="


