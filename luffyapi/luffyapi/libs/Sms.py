#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.conf import settings

AccessKeyId = settings.SMS_INFO.get('AccessKeyId')
AccessKeySecret = settings.SMS_INFO.get('AccessKeySecret')


def sms_codes(PhoneNumbers, code):
    client = AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', PhoneNumbers)
    request.add_query_param('SignName', "路飞学城")
    request.add_query_param('TemplateCode', "SMS_205139178")
    request.add_query_param('TemplateParam', code)

    response = client.do_action(request)
    # python2:  print(response)
    rest = str(response, encoding='utf-8')
    return rest
