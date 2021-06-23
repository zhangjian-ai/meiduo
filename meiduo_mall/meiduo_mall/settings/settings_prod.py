"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 添加导包路径，即配置app所在路径。app的默认位置是项目跟路径，可以方便添加注册app，少写路径；同时指定自定义的用户模型时，也需要用到
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j82ce(g6rqrs@(53u*go2mjk*-4k$j6%yl7-j)#^ihtcz@#s)^'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False


ALLOWED_HOSTS = ['www.meiduo.site', '121.4.47.229']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',  # cors跨域app
    'rest_framework',  # 添加rest_framework
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器上传图片模块
    'haystack',  # 对接elasticsearch搜索引擎的模块
    'rest_framework_swagger',  # 接口swagger。就是对coreapi进行了二次封装

    # 自定义用户app
    'users',
    'oauth',
    'areas',
    'goods',
    'content',
    'carts',
    'orders',
    'payment',

]

MIDDLEWARE = [
    # 解决跨域的中间件
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 指定路由文件
ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 设置模版路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {  # 解决swagger静态文件没有注册的问题，这里就是注册模版
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'meiduo_mall',
        'HOST': '121.4.47.229',
        'PORT': 3307,
        'USER': 'root',
        'PASSWORD': 'meiduo123'
    },
    'slave_01': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'meiduo_mall',
        'HOST': '121.4.47.229',
        'PORT': 3308,
        'USER': 'root',
        'PASSWORD': 'meiduo123'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# -------------------以下为项目新增或修改的配置------------------------

# 追加跨域白名单，指定那些域名可以访问后端接口
# CORS_ORIGIN_ALLOW_ALL = True  # 允许所有的ip访问后端接口
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://www.meiduo.site:8080',
    'http://www.meiduo.site:80',
    'http://121.4.47.229:80',
    'http://121.4.47.229:8080',
)
CORS_ALLOW_CREDENTIALS = True  # 跨域请求时允许携带cookie

# 修改默认的用户模型 应用名.模型名
AUTH_USER_MODEL = 'users.User'

# 本地化后台管理系统时区和语言
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

# django-redis 配置
CACHES = {
    "default": {  # 缓存省市区
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://121.4.47.229:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # 缓存session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://121.4.47.229:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_codes": {  # 缓存验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://121.4.47.229:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "home_category": {  # 缓存网站主页分类
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://121.4.47.229:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "home_content": {  # 缓存网站主页广告
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://121.4.47.229:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 缓存用户浏览记录
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://121.4.47.229:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "cart": {  # 缓存购物车
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://121.4.47.229:6379/6",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 省市区缓存配置
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}

# 配置日志打印及输出信息,在生成logger对象时，调用logger = logging.getLogger('django')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 定义日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 定义日志过滤器
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 定义日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',  # 打印到控制台的输出类
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 写入到文件、按日志文件大小划分的输出类
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo_mall.log"),  # 日志文件的位置
            'maxBytes': 20 * 1024 * 1024,  # 日志文件的大小
            'backupCount': 10,  # 日志文件最大备份数量，超过之后自动清理掉老得日志
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# 设置静态文件收集目录
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'meiduo_mall_frontend/meiduo_mall/static')
# Django访问静态文件的路径，相对于BASE_DIR
STATIC_URL = '/static/'
# 配置静态资源目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "/static/"),
]


# rest_framework 相关配置
REST_FRAMEWORK = {
    # 指定异常处理方法，在默认的异常处理方法上，新增了两种异常异常的处理
    'EXCEPTION_HANDLER': 'meiduo_mall.utils.exceptions.exception_handler',

    # JWT相关的认证类
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # 把JWT认证放第一位，则默认使用JWT进行认证
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),

    # 分页类
    'DEFAULT_PAGINATION_CLASS': 'meiduo_mall.utils.pagination.SetPagination',

    # 接口文档类
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

}

# JWT
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # 配置token过期时间

    # 指定重写后的视图jwt_response_payload_handler函数，增加需要的返回值
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}

# 配置自定义的认证后端
AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]

# QQ登录参数
QQ_CLIENT_ID = '101474184'
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

# 钉钉登陆参数
DT_APP_ID = '1199180434'
DT_APP_KEY = 'ding5uemblzjzfkdq11o'
DT_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
DT_CLIENT_SECRET = '5wnxEc2ILr3j7VTYB26U13KR3H4YcayPeT4MgfQDgYOL8v1WrTnx7AbXQfAAq_Oq'

# 邮件配置项
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
# 发送邮件的邮箱
EMAIL_HOST_USER = 'zj19180525254@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'EYBIOBDHLGLZHGZV'
# 收件人看到的发件人
EMAIL_FROM = '张老师<zj19180525254@163.com>'
# 这里未配置为True也会触发异常
EMAIL_USE_SSL = True

# 指定自定义的django文件存储类
DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.FastDFSStorage.FastDFSStorage'

# FastDFS
FDFS_URL = 'http://121.4.47.229:8888/'
FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')

# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,  # 编辑器高度
        # 'width': 300,  # 编辑器宽
    },
}
CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，使用了FastDFS，所以此处设为''。此处设置为空字符串，就会默认使用djangode文件保存路径

# 支付宝支付  dev
ALIPAY_APPID = "2021000117675026"
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do"
ALIPAY_DEBUG = True

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://121.4.47.229:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'meiduo',  # 指定elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 配置读写分离
DATABASE_ROUTERS = ['meiduo_mall.utils.db_router.MasterSlaveDBRouter']
