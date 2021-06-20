#!/bin/bash
# 从第一行到最后一行分别表示：
# 1. 生成数据库迁移文件
# 2. 根据数据库迁移文件来修改数据库
# 3. 用 uwsgi启动 django 服务, 不再使用python manage.py runserver
#python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
#uwsgi  --enable-threads uwsgi.ini
nohup uwsgi --ini uwsgi.ini &

# 保持容器内部有一个前台进程在运行,这里用消息队列保持
#while true
#do
#  sleep 1
#done
celery -A celery_tasks.main worker -l info
