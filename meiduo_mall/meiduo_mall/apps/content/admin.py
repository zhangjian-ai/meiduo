from django.contrib import admin
from django_redis import get_redis_connection

from . import models


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    """当广告内容发生变化时，清空对应的redis"""

    def save_model(self, request, obj, form, change):
        obj.save()
        # 创建redis链接对象
        redis_conn = get_redis_connection('home_category')
        redis_conn.clear()

    def delete_model(self, request, obj):
        obj.delete()
        # 创建redis链接对象
        redis_conn = get_redis_connection('home_category')
        redis_conn.clear()


admin.site.register(models.ContentCategory)
# admin.site.register(models.Content)
