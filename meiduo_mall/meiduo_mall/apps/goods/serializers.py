from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers

from .models import GoodsChannel, GoodsCategory, SKU, SKUImage, Goods
from .search_indexes import SKUIndex


class GoodsChannelSerializer(serializers.ModelSerializer):
    """频道序列化器"""

    category = serializers.StringRelatedField(label="顶级商品分类")

    class Meta:
        model = GoodsChannel
        # exclude = ['id', 'sequence', 'create_time', 'update_time']
        fields = ['category', 'url']


class GoodsCategorySerializer(serializers.ModelSerializer):
    """商品品类序列化器"""

    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']


class GoodsDetailSerializer(serializers.ModelSerializer):
    """商品的描述信息等"""

    class Meta:
        model = Goods
        fields = ['desc_detail', 'desc_pack', 'desc_service']


class SKUListSerializer(serializers.ModelSerializer):
    """SKU商品列表序列化器"""

    class Meta:
        model = SKU
        fields = ['id', 'name', 'caption', 'price', 'stock', 'market_price', 'comments', 'default_image_url']


class SKUImagesSerializer(serializers.ModelSerializer):
    """sku图片序列化器"""

    class Meta:
        model = SKUImage
        fields = ['image']


class SKUIndexSerializer(HaystackSerializer):
    """
    SKU索引结果数据序列化器
    """
    object = SKUListSerializer(read_only=True)

    class Meta:
        index_classes = [SKUIndex]
        fields = ('text', 'object')
