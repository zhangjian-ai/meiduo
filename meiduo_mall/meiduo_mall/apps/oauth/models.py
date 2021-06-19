from django.db import models
from meiduo_mall.utils.models import BaseModel
from users.models import User


class OAuthQQUser(BaseModel):
    """QQ登陆用户数据模型"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    openid = models.CharField(max_length=64, verbose_name="openid", db_index=True)  # db_index 表示创建表同时呢创建该字段的索引

    class Meta:
        db_table = "tb_oauth_qq"
        verbose_name = "QQ登陆用户数据"
        verbose_name_plural = verbose_name
