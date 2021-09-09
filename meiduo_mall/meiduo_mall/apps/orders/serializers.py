from decimal import Decimal
import logging
import random

from django.db import transaction
from django.utils import timezone
from django_redis import get_redis_connection
from rest_framework import serializers

from .models import OrderInfo, OrderGoods
from goods.models import SKU

logger = logging.getLogger('django')


class CommitOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ['order_id', 'address', 'pay_method', 'total_count', 'total_amount', 'freight']

        read_only_fields = ['order_id']
        extra_kwargs = {
            'address': {
                'write_only': True,
                'required': True
            },
            'pay_method': {
                'write_only': True,
                'required': True
            },
            'total_count': {
                'write_only': True,
                'required': True
            },
            'total_amount': {
                'write_only': True,
                'required': True
            },
            'freight': {
                'write_only': True,
                'required': True
            },

        }

    def create(self, validated_data):
        # 获取当前用户对象
        user = self.context['request'].user

        # 构造order_id
        order_id = timezone.now().strftime('%Y%m%d%H%M%S') + '%03d' % user.id + '%02d' % int(random.random() * 100)

        # 取出前端传入的数据
        address = validated_data.get('address')
        pay_method = validated_data.get('pay_method')
        total_count = validated_data.get('total_count')
        total_amount = validated_data.get('total_amount')
        freight = validated_data.get('freight')

        # 由于接下来会操作多张表，因此这里开启事物，避免产生脏数据
        with transaction.atomic():
            # 创建一个保存点
            save_id = transaction.savepoint()

            try:
                # 创建订单, create方法无需save
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=total_count,
                    total_amount=Decimal(total_amount),
                    freight=Decimal(freight),
                    pay_method=pay_method,
                    status=(OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                            if validated_data.get('pay_method') != OrderInfo.PAY_METHODS_ENUM['CASH']
                            else OrderInfo.ORDER_STATUS_ENUM['UNRECEIVED'])
                )

                # 获取订单商品详情
                redis_con = get_redis_connection('cart')
                # 获取缓存的待结算的全部商品
                skus = redis_con.lrange('%d' % user.id, 0, -1)

                # 修复同一sku不同规格无法购买的问题
                origin_sku_id = 0
                origin_count = 0

                for sku in skus:
                    # 为每个规格的sku生成一条订单详情数据
                    sku = sku.decode()
                    sku_id, spec = sku.split('_', 1)
                    while True:
                        # 获取当前sku对象
                        sku_obj = SKU.objects.get(id=sku_id)
                        # 从购物车缓存中获取当前规格产品的数量
                        count = int(redis_con.hget('cart_%d' % user.id, '%s_%s' % (sku_id, spec)))

                        if origin_sku_id != sku_id:
                            origin_sku_id = sku_id
                            origin_count = count
                        else:
                            origin_count += count

                        # 判断库存是否充足
                        origin_stock = sku_obj.stock
                        origin_sales = sku_obj.sales

                        if count > origin_stock:
                            # 如果库存不足，并抛出异常
                            # transaction.savepoint_rollback(save_id)
                            raise serializers.ValidationError('库存不足')

                        # 保存商品详情信息到数据库
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku_obj,
                            spec=spec,
                            count=count,
                            price=sku_obj.price
                        )

                        # 根据原始库存条件更新，返回更新的条目数，乐观锁
                        new_stock = origin_stock - origin_count
                        new_sales = origin_sales + origin_count
                        res = SKU.objects.get(id=sku_id, stock=origin_stock)
                        if res:
                            # 如果res等于0，说明该条sku已经被人修改了，就不能继续保存。但是剩余库存仍然能满足购买需要，所以这里跳出当前循环即可
                            res.stock = new_stock
                            res.sales = new_sales
                            res.save()
                        else:
                            continue

                        # 继续跟新SPU的销量
                        sku_obj.goods.sales += count
                        sku_obj.goods.save()

                        # 如果全部成功，则跳出当前while循环，继续创建下一个sku的详情记录
                        break

            except Exception as e:
                # 其他任何异常均回滚事物并引发
                logger.error(e)
                transaction.savepoint_rollback(save_id)
                raise

            # 如果一切ok那么就保存事物
            transaction.savepoint_commit(save_id)

            # 清空购物车中已生成订单的数据
            pl = redis_con.pipeline()
            for sku in skus:
                pl.hdel('cart_%d' % user.id, sku)
                pl.lrem('%d' % user.id, 0, sku)
            pl.execute()

            # 最后返回创建成功的订单
            return order


class SKUSerializer(serializers.ModelSerializer):
    """获取sku的部分信息"""

    class Meta:
        model = SKU
        fields = ['name', 'default_image_url']


class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单详情，具体的商品信息"""
    sku = SKUSerializer()

    class Meta:
        model = OrderGoods
        fields = ['sku', 'spec', 'count', 'price', 'score']


class OrderListSerializer(serializers.ModelSerializer):
    """订单查询序列化器"""
    skus = OrderGoodsSerializer(many=True)

    # chioce字段 get_<字段名>_display 显示名称
    status_text = serializers.CharField(source='get_status_display')

    class Meta:
        model = OrderInfo
        fields = ['order_id', 'total_count', 'total_amount', 'freight', 'status', 'skus', 'status_text']
