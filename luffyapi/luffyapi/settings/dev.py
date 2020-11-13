"""
Django settings for luffyapi project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 把apps路经注册到系统中
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1hucmsvn)@s2(duwje!o-t1sn-$(3t95356fbr!96o)8cn9l#t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',  # 跨域
    'rest_framework',  # drf框架的注册
    'xadmin',
    'crispy_forms',
    'reversion',
    'django_filters',  # 过滤组件，

    'home',  # app home注册
    'users',  # app users注册
    'course',  # app course注册
    'cart',  # app cart注册
    'order',  # app order注册
    'coupon',  # app coupon注册
    'payments',  # app payments注册

    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 富文本编辑器上传图片模块
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'luffyapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'luffyapi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'luffyapi',
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "luffy",
        "PASSWORD": "123456",
        "charset": "utf8",
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators


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

# 注册自定义用户模型，格式：“应用名.模型类名”
"""`AUTH_USER_MODEL` 参数的设置以`点.`来分隔，表示`应用名.模型类名`。"""
AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# 项目中存储上传文件的根目录[暂时配置]，注意，uploads目录需要手动创建否则上传文件时报错
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")  #
# 访问上传文件的url地址前缀
MEDIA_URL = "/media/"

# 日志配置
LOGGING = {
    'version': 1,  # 使用的python内置的logging模块，那么python可能会对它进行升级，所以需要写一个版本号，目前就是1版本
    'disable_existing_loggers': False,  # 是否去掉目前项目中其他地方中以及使用的日志功能，但是将来我们可能会引入第三方的模块，里面可能内置了日志功能，所以尽量不要关闭。
    'formatters': {  # 日志记录格式
        'verbose': {  # levelname等级，asctime记录时间，module表示日志发生的文件名称，lineno行号，message错误信息
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 过滤器：可以对日志进行输出时的过滤用的
        'require_debug_true': {  # 在debug=True下产生的一些日志信息，要不要记录日志，需要的话就在handlers中加上这个过滤器，不需要就不加
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {  # 和上面相反
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {  # 日志处理方式，日志实例
        'console': {  # 在控制台输出时的实例
            'level': 'DEBUG',  # 日志等级；debug是最低等级，那么只要比它高等级的信息都会被记录
            'filters': ['require_debug_true'],  # 在debug=True下才会打印在控制台
            'class': 'logging.StreamHandler',  # 使用的python的logging模块中的StreamHandler来进行输出
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/luffy.log"),  # 注意，你的文件应该有读写权限。
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
    },
    # 日志对象
    'loggers': {
        'django': {  # 和django结合起来使用，将django中之前的日志输出内容的时候，按照我们的日志配置进行输出，
            'handlers': ['console', 'file'],  # 将来项目上线，把console去掉
            'propagate': True,
            # 冒泡：是否将日志信息记录冒泡给其他的日志处理系统，工作中都是True，不然django这个日志系统捕获到日志信息之后，其他模块中可能也有日志记录功能的模块，就获取不到这个日志信息了
        },
    }
}

# 异常处理
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'luffyapi.utils.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

# 配置JWT JWT_EXPIRATION_DELTA 指明token的有效期

JWT_AUTH = {
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=30),
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}

AUTHENTICATION_BACKENDS = [
    'users.utils.CustomeModelBackend',
]

"""
跨域CORS设置
CORS_ORIGIN_ALLOW_ALL为True，指定所有域名（ip）都可以访问后端接口，默认为False
CORS_ORIGIN_WHITELIST指定能够访问后端接口的ip或域名列表
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://192.168.13.254:8080'
]
"""
CORS_ORIGIN_ALLOW_ALL = True

# CORS_ALLOW_CREDENTIALS允许跨域时携带Cookie，默认为False
CORS_ALLOW_CREDENTIALS = False

# django admin设
# 修改使用中文界面
LANGUAGE_CODE = 'zh-Hans'

# 修改时区
TIME_ZONE = 'Asia/Shanghai'
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# 腾讯防水墙配置
TENCENT_CAPTCHA = {
    "GATEWAY": "https://ssl.captcha.qq.com/ticket/verify",
    "APPID": "2021539286",
    "App_Secret_Key": "0UNkPIA8yP_cjiLubTSKaJQ**",
}


# 阿里云短信接口
SMS_INFO = {
    'AccessKeyId': 'LTAI4G9wKSbTB5dyDYhGNRLV',
    'AccessKeySecret': 'zUGaBxFzrWyHv2bE6oIbvit3vnzuGl',
}


# 支付宝配置信息
ALIAPY_CONFIG = {
    # "gateway_url": "https://openapi.alipay.com/gateway.do?", # 真实支付宝网关地址
    "gateway_url": "https://openapi.alipaydev.com/gateway.do?",  # 沙箱支付宝网关地址
    "appid": "2016102600767166",  # 沙箱中那个应用id
    "app_notify_url": None,
    "app_private_key_path": os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem"),
    "alipay_public_key_path": os.path.join(BASE_DIR, "apps/payments/keys/alipay_public_key.pem"),
    "sign_type": "RSA2",
    "debug": False,
    "return_url": "http://www.luffycity.com:8080/payments/result",  # 同步回调地址
    "notify_url": "http://www.luffycity.com:8000/payments/result/",  # 异步结果通知
}

# 设置redis缓存
CACHES = {
    # 默认缓存
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 项目上线时,需要调整这里的路径
        # "LOCATION": "redis://127.0.0.1:6379/0",
        "LOCATION": "redis://:123456@127.0.0.1:6379/0",
        # 如果redis设置密码的话，需要以这种格式host前面是密码

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 提供给xadmin或者admin的session存储
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:123456@127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 提供存储短信验证码
    "sms_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:123456@127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 提供给购物车使用
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:123456@127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 设置xadmin用户登录时,登录信息session保存到redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"


# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能,full表示全部，Basic表示基本功能，功能少很多，还有个Custom自定义功能选项
        'height': 300,      # 编辑器高度
        # 'width': 300,     # 编辑器宽
    },
}
CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，留空则调用django的文件上传功能