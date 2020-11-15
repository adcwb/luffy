from mycelery.main import app
from order.models import Order
import datetime
from luffyapi.settings import constants


@app.task(name='cancle_order')
def cancle_order():
    expire_time = constants.ORDER_EXPIRE_TIME
    # 下单时间 < 当前时间 - 过期间隔
    current_time = datetime.datetime.now()

    expire_order_list = Order.objects.filter(order_status=0,
                                             pay_time__lt=current_time - datetime.timedelta(seconds=expire_time))

    for order in expire_order_list:
        order.order_status = 3
        order.save()
