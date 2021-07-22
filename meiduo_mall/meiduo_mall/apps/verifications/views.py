import random
import logging

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_mall.libs import constants

from celery_tasks.sms import tasks

logger = logging.getLogger('django')


class SMSCodeView(APIView):
    """
    发送短信验证码
    """

    def get(self, request, mobile):
        # 创建redis链接对象
        redis_conn = get_redis_connection('verify_codes')

        # 校验60s内不能重复发送短信
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({"code": 1, "msg": "发送短信过于频繁，请稍后再试。"})

        # 生成验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)

        # 创建redis管道并写入验证码、发送标识和他们的过期时间
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 管道执行
        pl.execute()

        # 调用异步任务函数，执行异步发短信
        # tasks.send_sms_code(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
        #                     constants.SEND_SMS_TEMPLATE_ID)  # 普通调用

        # 异步调用
        tasks.send_sms_code.delay(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
                                  constants.SEND_SMS_TEMPLATE_ID)

        return Response({"sms_code": sms_code, 'msg': '短信验证码发送成功'})

        # # 发送短信
        # result = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
        #                         constants.SEND_SMS_TEMPLATE_ID)

        # if result == 0:
        #     # 创建redis管道并写入验证码、发送标识和他们的过期时间
        #     pl = redis_conn.pipeline()
        #     pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        #     pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        #
        #     # 管道执行
        #     pl.execute()
        #
        #     # 响应发送短信验证码结果
        #     return Response({"code": 0, "msg": "验证码发送成功"})
        #
        # return Response({"code": 1, "msg": "验证码发送失败，请稍后再试"}, status=status.HTTP_400_BAD_REQUEST)
