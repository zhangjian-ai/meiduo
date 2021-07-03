from django.db import models
from django.contrib.auth.models import AbstractUser

from meiduo_mall.utils.models import BaseModel
from meiduo_mall.utils.tools import SecretTool, create_jwt_token


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号码")
    email_active = models.BooleanField(default=False, verbose_name="邮箱认证")

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_verify_email_url(self):
        """在模型类中写入生成验证邮箱的地址，那么在视图或者序列化器中，就可以通过模型对象直接调用"""
        data = {'id': self.id, 'email': self.email}
        token = SecretTool.encryption(data)

        verify_url = 'http://www.meiduo.site:8080/usercenter/verify_email?token=' + token

        return verify_url

    @staticmethod
    def check_verify_email_token(token):
        """验证邮箱token"""
        # 解密token，这里会校验token是否过期
        data = SecretTool.decryption(token)

        if data is None:
            return data

        # 根据token中的信息，查找用户是否存在
        id = data.get('id')
        email = data.get('email')

        try:
            user = User.objects.get(id=id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=10, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=50, null=True, blank=True, default='', verbose_name='邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')
    is_default = models.BooleanField(default=False, verbose_name='默认地址')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
        ordering = ['-is_default', '-update_time']
