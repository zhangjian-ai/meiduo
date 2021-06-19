from rest_framework import serializers

from goods.models import SKU


class CartSerializer(serializers.Serializer):
    """添加购物车序列化器"""
    sku_id = serializers.IntegerField(label="sku_id", min_value=1)
    count = serializers.IntegerField(label="sku数量", min_value=1)
    spec = serializers.CharField(label="sku规格", allow_null=True)

    def validate(self, attrs):
        try:
            SKU.objects.get(id=attrs['sku_id'])
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        return attrs


class CartSKUSerializer(serializers.ModelSerializer):
    """查询购物车"""

    count = serializers.IntegerField(label="数量", min_value=1)
    spec = serializers.CharField(label="规格")

    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'stock', 'count', 'spec', 'default_image_url']
