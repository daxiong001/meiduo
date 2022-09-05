import logging

from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler

from meiduo.utils.myresponse import APIResponse

logger = logging.getLogger('django')


def exception_handler(exc, context):
    """
    :param exc:异常实例对象
    :param context:抛出异常的上下文（包含request和view对象）
    :return: response响应对象
    """
    res = drf_exception_handler(exc, context)

    if res is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            logger.error('[%s] %s' % (view, exc))
            return APIResponse(data={"message": '数据库或redis错误', "msg": 500}, status=status.HTTP_507_INSUFFICIENT_STORAGE, code=500)
        else:
            logger.error('[%s] %s' % (view, exc))
            return APIResponse({"message": '服务器未知错误', "msg": 500}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    else:
        return APIResponse(code=500, exception=True, desc=res.data, success=False)
