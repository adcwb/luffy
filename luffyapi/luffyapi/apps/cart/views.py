from django.shortcuts import render
from rest_framework.viewsets import ViewSet
# Create your views here.
from django_redis import get_redis_connection
from course import models
from rest_framework.response import Response
from rest_framework import status
from luffyapi.settings import constants
from rest_framework.permissions import IsAuthenticated

import logging

logger = logging.getLogger('django')


class AddCartView(ViewSet):
    permission_classes = [IsAuthenticated, ]  # 请求头里面必须带着token

    def add(self, request):

        course_id = request.data.get('course_id')
        # user_id = 1
        user_id = request.user.id

        expire = 0  # 表示永久有效
        conn = get_redis_connection('cart')

        try:
            models.Course.objects.get(id=course_id)
        except:

            return Response({'msg': '课程不存在'}, status=status.HTTP_400_BAD_REQUEST)

        # set type
        '''
        user_id:{
            course_id:expire,
            course_id:expire,
        }

        '''

        pipe = conn.pipeline()  # 创建管道,
        pipe.multi()

        # 批量操作
        pipe.hset('cart_%s' % user_id, course_id, expire)
        # pipe.hset('cart_%s'%user_id, course_id , expire)
        # pipe.hset('cart_%s'%user_id, course_id , expire)
        # pipe.hset('cart_%s'%user_id, course_id , expire)

        pipe.execute()

        # conn.sadd('cart_%s'%user_id, course_id)
        # cart_length = conn.scard('cart_%s'%user_id)
        cart_length = conn.hlen('cart_%s' % user_id)
        print('cart_length', cart_length)

        return Response({'msg': '添加成功', 'cart_length': cart_length})

    def cart_list(self, request):
        # requset.user
        # print('>>>>>>>>>>>>>>>', request.user)
        # user_id = 1
        user_id = request.user.id

        conn = get_redis_connection('cart')

        conn.delete('selected_cart_%s' % user_id)
        ret = conn.hgetall('cart_%s' % user_id)  # dict {b'1': b'0', b'2': b'0'}
        cart_data_list = []
        # print(ret)
        try:
            for cid, eid in ret.items():
                course_id = cid.decode('utf-8')
                expire_id = eid.decode('utf-8')

                course_obj = models.Course.objects.get(id=course_id)

                cart_data_list.append({
                    'course_id': course_obj.id,
                    'name': course_obj.name,
                    'course_img': constants.SERVER_ADDR + course_obj.course_img.url,
                    'price': course_obj.price,
                    'real_price': course_obj.real_price(),
                    'expire_id': expire_id,
                    'selected': False,  # 默认没有勾选
                })
        except Exception:
            logger.error('获取购物车数据失败')
            return Response({'msg': '后台数据库出问题了,请联系管理员'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
            # try:
        #     models.Course.objects.filter()
        # print(cart_data_list)

        return Response({'msg': 'xxx', 'cart_data_list': cart_data_list})

    def change_select(self, request):
        course_id = request.data.get('course_id')

        try:
            models.Course.objects.get(id=course_id)
        except:
            return Response({'msg': '课程不存在，不要乱搞！'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        conn = get_redis_connection('cart')  # 1:{1,3}
        conn.sadd('selected_cart_%s' % user_id, course_id)

        return Response({'msg': '恭喜你！勾选成功！'})

    def cancel_select(self, request):
        course_id = request.data.get('course_id')

        try:
            models.Course.objects.get(id=course_id)
        except:
            return Response({'msg': '课程不存在，不要乱搞！'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        conn = get_redis_connection('cart')  # 1:{1,3}
        conn.srem('selected_cart_%s' % user_id, course_id)

        return Response({'msg': '恭喜你！少花钱了，但是你真的不学习了吗！'})
