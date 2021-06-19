import logging
import random
import string

from rest_framework import serializers
from django_redis import get_redis_connection

from meiduo_mall.utils.tools import SecretTool

from users.models import User
from .models import OAuthQQUser

logger = logging.getLogger('django')


class QQAuthUserSerializer(serializers.Serializer):
    """
    QQ登陆创建用户序列化器
    由于OAuthQQUser模型中可用字段较少，这里直接定义一个序列化器
    """
    openid = serializers.CharField(label="操作凭证")
    mobile = serializers.RegexField(label="手机号", regex=r'^1[3-9]\d{9}$')  # 按正则校验手机号
    password = serializers.CharField(label="密码", max_length=20, min_length=8)
    sms_code = serializers.CharField(label="短信验证码")

    def validate(self, attrs):
        # 获取并解密前端返回的openid
        openid = SecretTool.decryption(attrs.pop('openid'))
        if openid is None:
            logger.info('无效的openid')
            raise serializers.ValidationError('无效的openid')

        attrs['openid'] = openid

        # 校验短信验证码是否正确
        mobile = attrs.get('mobile')
        sms_code = attrs.pop('sms_code')

        redis_conn = get_redis_connection('verify_codes')
        real_code = redis_conn.get('sms_%s' % mobile).decode()

        if sms_code != real_code:
            logger.info('验证码错误')
            raise serializers.ValidationError('验证码错误')

        # 校验通过后，判断用户是否存在
        try:
            user = User.objects.get(mobile=mobile)
        except Exception:
            pass  # 如果不存在，则在create中创建用户
        else:
            # 如果存在则检查密码是否正确
            password = attrs.get('password')

            if not user.check_password(password):
                logger.info('密码错误')
                raise serializers.ValidationError('密码错误')

            attrs['user'] = user  # 添加user对象，传入create

        return attrs

    def create(self, validated_data):
        # 获取用户
        user = validated_data.get('user')

        if not user:
            # 用户不存在，则新增一条用户信息。这里创建了一个用户对象，不会直接保存到User表中
            password = validated_data.get('password')
            user = User(
                username=validated_data.get('mobile'),
                mobile=validated_data.get('mobile'),
            )
            user.set_password(password)
            user.save()

        # 创建用户和QQ的关联关系
        OAuthQQUser.objects.create(
            openid=validated_data.get('openid'),
            user=user  # 如果外键传入的是一个外键对象，则根据model字段指明对象即可，不需要按实际字段名指定
        )

        return user  # 返回user，序列化器的save()方法会拿到该值并继续返回

