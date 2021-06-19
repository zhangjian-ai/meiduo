import logging
from celery_tasks.main import celery_app
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger('django')


@celery_app.task(name='send_verify_email')  # 给异步任务起别名
def send_verify_email(to_email: list, verify_url: str):
    """
    发送验证邮件
    """
    try:
        # 邮件标题
        subject = "美多商城邮箱验证"

        # 邮件内容，这里是采用超文本
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)

        # 发送邮件
        send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)

    except Exception as e:
        logger.error("邮件发送异常: %s。邮箱列表：%s" % (str(e), to_email))
    else:
        logger.info("邮件发送成功。邮箱列表：%s" % to_email)
