from celery import Celery
from importlib import import_module

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')
import django

django.setup()

# 创建celery实例对象
app = Celery()
# 通过app对象加载配置，文件路径
app.config_from_object('mycelery.config')

# 自动搜索并加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
app.autodiscover_tasks(['mycelery.sms', ])
#会自动识别sms目录下面的tasks.py文件中的任务，所以不需写成mycelery.sms.tasks

# python main.py
