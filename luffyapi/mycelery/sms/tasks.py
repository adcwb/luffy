# 任务的文件，名称必须是这个!!!
from mycelery.main import app
# from ..main import app

from luffyapi.libs import Sms
from django.conf import settings
from luffyapi.settings import constants


import logging
logger = logging.getLogger('django')
AccessKeyId = settings.SMS_INFO.get('AccessKeyId')
AccessKeySecret = settings.SMS_INFO.get('AccessKeySecret')

# name表示设置任务的名称，如果不填写，则默认使用函数名(路径)做为任务名
@app.task(name='sms_codes')
def sms_codes(phone, sms_code_tmp):

    # todo 发送验证码
    res = Sms.sms_codes(phone, sms_code_tmp)
    if not res:
        logger.error('{}手机号短信发送失败'.format(phone))
    return '短信发送成功啦'


@app.task
def sms_code2():
    print('xxxxx2')
    return '发送短信成功2'


