import random
import re

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
# Create your views here.
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status
from users.serializers import CustomeSerializer, RegisterModelSerializer
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
    serializer_class = RegisterModelSerializer


from django_redis import get_redis_connection


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
        print(sms_code)

        # 保存验证码

        conn.setex('mobile_%s' % phone, constants.SMS_CODE_EXPIRE_TIME, sms_code)  # 设置有效期

        #
        conn.setex('mobile_interval_%s' % phone, constants.SMS_CODE_INTERVAL_TIME, sms_code)  # 设置发送短信的时间间隔

        # todo 发送验证码
        #
        return Response({'msg': 'ok'})
