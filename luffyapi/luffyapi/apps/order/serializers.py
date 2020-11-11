import datetime

from rest_framework import serializers
from . import models
from django_redis import get_redis_connection

from course.models import Course
from course.models import CourseExpire
from coupon.models import UserCoupon, Coupon
from django.db import transaction



class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id', 'order_number', 'pay_type', 'coupon', 'credit']

        extra_kwargs = {
            'id':{'read_only':True},
            'order_number':{'read_only':True},
            'pay_type':{'write_only':True},
            'coupon':{'write_only':True},
            'credit':{'write_only':True},
        }

    def validate(self, attrs):

        # 支付方式
        pay_type = int(attrs.get('pay_type',0))  #

        if pay_type not in [i[0] for i in models.Order.pay_choices]:
            raise serializers.ValidationError('支付方式不对！')


        # todo 优惠券校验，看看是否过期了等等
        coupon_id = attrs.get('coupon', 0)
        if coupon_id > 0:

            try:
                user_conpon_obj = UserCoupon.objects.get(id=coupon_id)
            except:
                raise serializers.ValidationError('订单创建失败，优惠券id不对')
            # condition = user_conpon_obj.coupon.condition
            now = datetime.datetime.now().timestamp()
            start_time = user_conpon_obj.start_time.timestamp()
            end_time = user_conpon_obj.end_time.timestamp()
            if now < start_time or now > end_time:
                raise serializers.ValidationError('订单创建失败，优惠券不在使用范围内，滚犊子')


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

            total_price = 0  #总原价
            total_real_price = 0  # 总真实价格

            with transaction.atomic():  # 添加事务
                sid = transaction.savepoint()  #创建事务保存点
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

                        total_price += course_obj.price
                        total_real_price += course_obj.real_price(expire_id)

                coupon_id = validated_data.get('coupon')
                try:
                    user_conpon_obj = UserCoupon.objects.get(id=coupon_id)
                except:
                    transaction.rollback(sid)
                    raise serializers.ValidationError('订单创建失败，优惠券id不对')
                condition = user_conpon_obj.coupon.condition

                if total_real_price < condition:
                    transaction.rollback(sid)
                    raise serializers.ValidationError('订单创建失败，优惠券不满足使用条件')
                sale = user_conpon_obj.coupon.sale
                if sale[0] == '-':
                    total_real_price -= float(sale[1:])
                elif sale[0] == '*':
                    total_real_price *= float(sale[1:])

                order_obj.total_price = total_price
                order_obj.real_price = total_real_price
                order_obj.save()
                # 结算成功之后，再清除
                # conn = get_redis_connection('cart')
                # conn.delete('selected_cart_%s' % user_id)

            # print('xxxxx')
        except Exception:
            raise models.Order.DoesNotExist

        return order_obj



