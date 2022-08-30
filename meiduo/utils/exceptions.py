import logging

from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger('django')


def exception_handler(exc, context):
    """
    :param exc:异常实例对象
    :param context:抛出异常的上下文（包含request和view对象）
    :return: response响应对象
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            logger.error('[%s] %s' % (view, exc))
            response = Response({"message": '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response