from rest_framework.views import exception_handler

from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework import status
from redis import RedisError

import logging
logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常类
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = exception_handler(exc, context)

    if response is None:
        view = context['view']   # 错误出现的那个函数或者方法
        if isinstance(exc, DatabaseError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        # if isinstance(exc, RedisError):
        #     # redis数据库异常
        #     logger.error('[%s] %s' % (view, exc))
        #     response = Response({'message': 'Redis数据库内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        #
        # if isinstance(exc,Exception):
        #     # 未知异常
        #     logger.error("发生未知异常。view=%s，exc=%s" % (view, exc))
        #     response = Response({'detail': '服务器出现未知错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    return response