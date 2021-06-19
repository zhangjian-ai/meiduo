from celery import Celery

# 在celery_tasks上级目录执行命令启动异步服务
# celery -A celery_tasks.main worker -l info
# -A：指定worker -l：指定日志输出级别

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.settings_dev'

# 创建celery应用对象
celery_app = Celery('meiduo')  # 入参是为该对象起了一个别名

# 导入celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])  # 自动获取sms文件夹下名为task.py的文件里的任务注册
