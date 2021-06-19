import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from celery_tasks.email.tasks import send_verify_email
from .models import User, Address
from meiduo_mall.utils.tools import create_jwt_token
from goods.models import SKU
from meiduo_mall.libs import constants


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""

    password2 = serializers.CharField(label="确认密码", write_only=True)
    sms_code = serializers.CharField(label="验证码", write_only=True)
    allow = serializers.CharField(label="是否同意协议", write_only=True)

    # 新增一个token字段，用于向前端传递token信息。该字段是模型中没有的字段，需要在序列化之前给模型对象中写入该值
    token = serializers.CharField(label="Token", read_only=True)

    class Meta:
        model = User  # 指定从User模型中映射序列化字段

        # -----------序列化、反序列化 字段分析------------
        # 前端传入的字段 ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
        # 模型中已有的字段 ['id', 'username', 'password', 'mobile',]

        # 需要序列化返回给前端的字段 ['id', 'username', 'mobile', 'token']   id是默认在模型中的，所以视图对象是有这个字段的; token是单独加的
        # 需要反序列化的字段 ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']    ---其实就是前端传入的都要反序列化

        # 除去模型中已有的字段，还需要添加三个反序列化的字段(网上看)；并修改password只发序列化，同时优化用户名、密码的校验长度

        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow', 'token']
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):
        """单独校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号有误')
        return value

    def validate_allow(self, value):
        """校验是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请先同意使用协议')
        return value

    def validate(self, attr):
        """校验两次密码是否相同"""
        if attr.get('password') != attr.get('password2'):
            raise serializers.ValidationError('两个密码不一致')

        # 检查验证码是否正确
        redis_conn = get_redis_connection('verify_codes')
        mobile = attr.get('mobile')
        real_sms_code = redis_conn.get('sms_%s' % mobile)

        # redis存储的字符串默认一byte类型保存，所以取出来需要解码一下
        if real_sms_code is None or attr.get('sms_code') != real_sms_code.decode():
            raise serializers.ValidationError('验证码错误或已经过期')

        return attr

    def create(self, validated_data):
        """重写create方法"""
        # 删除不需要存入数据库的字段
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        # 取出前端传过来的密码
        password = validated_data.pop('password')

        # 创建用户模型对象，给mobile、username赋值
        user = User(**validated_data)
        user.set_password(password)  # 把密码加密后在赋值给user对象的password字段

        user.save()  # 保存到数据库

        # 返回数据之前，给模型增加token字段
        token = create_jwt_token(user)

        user.token = token

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """因为要序列化的字段，在模型中都是有的，这里就直接继承ModelSerializer进行映射"""

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'email_active']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

        extra_kwargs = {
            'email': {
                'required': True
            }
        }

    # 此处是修改邮箱，父类update可以直接完成任务。但此处，我们还希望添加邮箱之后，发送邮箱认证邮件
    def update(self, instance, validated_data):
        # 更新邮箱
        setattr(instance, 'email', validated_data.get('email'))
        instance.save()

        # 发送邮件。邮件中构建一个包含用户信息的token，方便后续验证
        verify_url = instance.generate_verify_email_url()

        # 发送邮件
        send_verify_email.delay(validated_data.get('email'), verify_url)

        return instance


class UserAddressSerializer(serializers.ModelSerializer):
    # 外键字段默认序列化出外键对象的id，这里修改成其__str__方法的返回值，即直接获得省市区的名称
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)

    # 外键字段写入时，可以传入对应的外键对象，但此处前端传入的都是id，所以再新增三个写入的字段
    # 外键再当前表中实际字段名是：外键名_id，所以直接写入值时，要指明其真实的字段名。。而传入对象时，则按模型名传入对象即可
    province_id = serializers.IntegerField(label="省ID", required=True)
    city_id = serializers.IntegerField(label="市ID", required=True)
    district_id = serializers.IntegerField(label="区ID", required=True)

    class Meta:
        model = Address
        exclude = ['user', 'is_deleted', 'update_time', 'create_time']

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError('手机号错误')
        return attrs

    def create(self, validated_data):
        # 获取视图的传参。这里故意不序列化user，通过这种方式传值
        validated_data['user'] = self.context
        return super().create(validated_data)


class EditAddressTitleSerializer(serializers.ModelSerializer):
    """修改地址标题序列化器"""

    class Meta:
        model = Address
        fields = ['title']


class UserBrowsingHistorySerializer(serializers.Serializer):
    """保存用户浏览记录序列化器"""

    sku_id = serializers.IntegerField(label="sku_id", min_value=1)

    def validate_sku_id(self, value):
        # """检验sku是否合法"""
        try:
            SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('sku不存在')

        return value

    def create(self, validated_data):
        # 利用序列化器create函数，把数据存到redis

        # 获取redis链接
        redis_con = get_redis_connection('history')
        # 获取用户对象，该方法只能在视图是GenericView及其子类时有效，因为请求对象是在其内部的get_serializer中包装进去的
        user_id = self.context['request'].user.id

        pl = redis_con.pipeline()
        sku_id = validated_data.get('sku_id')
        # 先移除当前sku已经存在的记录
        pl.lrem('history_%d' % user_id, 0, sku_id)

        # 添加记录
        pl.lpush('history_%d' % user_id, sku_id)

        # 仅保留最新的5条
        pl.ltrim('history_%d' % user_id, 0, constants.USER_MAX_BROWSING_HISTORY_COUNT - 1)

        pl.execute()

        return validated_data


class SKUSerializer(serializers.ModelSerializer):
    """SKU历史记录序列化器"""

    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'comments', 'default_image_url']