FROM python:3.8
# 在容器内/var/www/html/下创建 工作文件夹
RUN mkdir -p /var/www/html/meiduo_mall
# 将当前目录文件加入到容器工作目录中（. 表示当前Dockerfile宿主机目录）
COPY . /var/www/html/meiduo_mall/
# 设置容器内工作目录,后续的RUN等命令，在容器内部执行安装
WORKDIR /var/www/html/meiduo_mall
# 下载第三方包
RUN pip3 install https://github.com/darklow/django-suit/tarball/v2 \
&& pip3 install -i https://pypi.doubanio.com/simple uwsgi
RUN pip3 install -i https://pypi.doubanio.com/simple -r requirements.txt \
# 设置start.sh文件可执行权限
&& chmod +x ./start.sh \
# Windows环境下编写的start.sh每行命令结尾有多余的\r字符，需移除。
&& sed -i 's/\r//' ./start.sh
# 启动容器时运行脚本
CMD ./start.sh
