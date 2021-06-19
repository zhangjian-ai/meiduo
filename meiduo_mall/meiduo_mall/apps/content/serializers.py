from rest_framework import serializers
from .models import Content, ContentCategory


class ContentSerializer(serializers.ModelSerializer):
    """广告序列化器"""

    class Meta:
        model = Content
        exclude = ['update_time', 'create_time', 'status', 'category']


class ContentCategorySerializer(serializers.ModelSerializer):
    """广告类别序列化器"""

    # 由于还要过滤掉广告中status != 1 的数据，所以这里直接序列化不太好，在视图中将筛选好查询集，在序列化具体的广告内容
    # content_set = ContentSerializer(label="广告内容", many=True)

    class Meta:
        model = ContentCategory
        exclude = ['update_time', 'create_time']

