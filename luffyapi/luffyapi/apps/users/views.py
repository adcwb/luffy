import random
import re
import logging

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
# Create your views here.
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status
from .serializers import CustomeSerializer, RegisterModelSerializer
from .utils import get_user_obj
from . import models
from luffyapi.settings import constants


# Create your views here.

# from luffyapi.apps.users.serializers import CustomeSerializer


class CustomLoginView(ObtainJSONWebToken):
    serializer_class = CustomeSerializer


class CheckPhoneNumber(APIView):

    def get(self, request):
        phone_number = request.GET.get('phone')

        if not re.match('^1[3-9][0-9]{9}$', phone_number):
            # g格式不对
            return Response({'error_msg': '手机号格式有误，请重新输入！'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证唯一性
        ret = get_user_obj(phone_number)
        if ret:
            return Response({'error_msg': '手机号已被注册，请换手机号'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'msg': 'ok'})


class RegisterView(CreateAPIView):
    queryset = models.User.objects.all()
    print(queryset)
    serializer_class = RegisterModelSerializer


from django_redis import get_redis_connection
# from  luffyapi.libs.Sms import sms_codes
from mycelery.sms.tasks import sms_codes

class GetSMSCodeView(APIView):

    def get(self, request, phone):
        # 验证是否已经发送过短信了
        conn = get_redis_connection('sms_code')
        ret = conn.get('mobile_interval_%s' % phone)
        print(ret)

        if ret:
            return Response({'msg': '60秒内已经发送过了，别瞎搞'}, status=status.HTTP_400_BAD_REQUEST)

        # 生成验证码
        sms_code = "%06d" % random.randint(0, 999999)
        sms_code_tmp = {"code": sms_code}
        print(sms_code_tmp)


        # 保存验证码

        conn.setex('mobile_%s' % phone, constants.SMS_CODE_EXPIRE_TIME, sms_code)  # 设置有效期

        #
        conn.setex('mobile_interval_%s' % phone, constants.SMS_CODE_INTERVAL_TIME, sms_code)  # 设置发送短信的时间间隔

        #  发送验证码
        # res = sms_codes(phone, sms_code_tmp)
        sms_codes.delay(phone, sms_code_tmp)
        # logger = logging.getLogger('django')
        # if not res:
        #     logger.error('{}手机号短信发送失败'.format(phone))
        #     return Response({'msg': '短信发送失败，请联系管理员'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'ok'})
