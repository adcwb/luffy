import datetime

from rest_framework import serializers
from . import models
from django_redis import get_redis_connection

from course.models import Course
from course.models import CourseExpire
from django.db import transaction


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id', 'order_number', 'pay_type', 'coupon', 'credit']

        extra_kwargs = {
            'id': {'read_only': True},
            'order_number': {'read_only': True},
            'pay_type': {'write_only': True},
            'coupon': {'write_only': True},
            'credit': {'write_only': True},
        }

    def validate(self, attrs):

        # 支付方式
        pay_type = int(attrs.get('pay_type', 0))  #

        if pay_type not in [i[0] for i in models.Order.pay_choices]:
            raise serializers.ValidationError('支付方式不对！')

        # todo 优惠券校验，看看是否过期了等等

        # todo 积分上限校验

        return attrs

    def create(self, validated_data):
        try:
            # 生成订单号  [日期，用户id，自增数据]
            current_time = datetime.datetime.now()
            now = current_time.strftime('%Y%m%d%H%M%S')
            user_id = self.context['request'].user.id
            conn = get_redis_connection('cart')
            num = conn.incr('num')
            order_number = now + "%06d" % user_id + "%06d" % num

            with transaction.atomic():  # 添加事务

                # 生成订单
                order_obj = models.Order.objects.create(**{
                    'order_title': '31期订单',
                    'total_price': 0,
                    'real_price': 0,
                    'order_number': order_number,
                    'order_status': 0,
                    'pay_type': validated_data.get('pay_type', 0),
                    'credit': 0,
                    'coupon': 0,
                    'order_desc': '女朋友',
                    'pay_time': current_time,
                    'user_id': user_id,
                    # 'user':user_obj,
                })

                select_list = conn.smembers('selected_cart_%s' % user_id)

                ret = conn.hgetall('cart_%s' % user_id)  # dict {b'1': b'0', b'2': b'0'}

                for cid, eid in ret.items():
                    expire_id = int(eid.decode('utf-8'))
                    if cid in select_list:

                        course_id = int(cid.decode('utf-8'))
                        course_obj = Course.objects.get(id=course_id)
                        # expire_text = '永久有效'
                        if expire_id > 0:
                            expire_text = CourseExpire.objects.get(id=expire_id).expire_text

                        # 生成订单详情
                        models.OrderDetail.objects.create(**{
                            'order': order_obj,
                            'course': course_obj,
                            'expire': expire_id,
                            'price': course_obj.price,
                            'real_price': course_obj.real_price(expire_id),
                            'discount_name': course_obj.discount_name(),
                        })
            # print('xxxxx')
        except Exception:
            raise models.Order.DoesNotExist

        return order_obj
