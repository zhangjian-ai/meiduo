import logging
from celery_tasks.main import celery_app
from celery_tasks.sms.yuntongxun.sms import CCP

logger = logging.getLogger('django')


@celery_app.task(name='send_sms_code')  # 给异步任务起别名
def send_sms_code(mobile, datas, temp_id):
    """
     发送短信验证码
    :param mobile: 手机号
    :param datas: [验证码, 过期时间]
    :param temp_id: 有效期
    :return: None
    """
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile, datas, temp_id)
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    else:
        if result == 0:
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
