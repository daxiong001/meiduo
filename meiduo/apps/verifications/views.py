import logging
from random import randint

from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from . import constants
from celery_tasks.sms.tasks import send_sms_code

logger = logging.getLogger('django')


class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1、创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 先从redis获取发送标记
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({"message": "手机号频繁发送短信"}, status=status.HTTP_400_BAD_REQUEST)
        sms_code = '%06d' % randint(0, 999999)
        logger.info("获取手机发送验证码：" + sms_code)
        #   创建redis管道，把多次redis操作装入管道中，将来一次性去执行，减少redis连接操作
        pl = redis_conn.pipeline()

        # 2、把验证码存储到redis数据库
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 执行redis管道，一般只把赋值的加入管道
        pl.execute()

        # 3、触发异步任务，将异步任务添加到celery任务队列
        send_sms_code.delay(mobile, sms_code)
        # 4、响应
        return Response({'message': 'ok'})
