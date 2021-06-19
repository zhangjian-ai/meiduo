from django.contrib import admin
from django_redis import get_redis_connection

from . import models


@admin.register(models.GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    """当商品类型发生变化时，清空对应的redis"""

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


# admin.site.register(models.GoodsCategory)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Goods)
admin.site.register(models.Brand)
admin.site.register(models.GoodsSpecification)
admin.site.register(models.SpecificationOption)
admin.site.register(models.SKU)
admin.site.register(models.SKUSpecification)
admin.site.register(models.SKUImage)
