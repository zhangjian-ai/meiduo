from rest_framework import serializers
from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """当前行政区序列化器"""

    class Meta:
        model = Area
        fields = ['id', 'name']


class SubsAreaSerializer(serializers.ModelSerializer):
    """当前行政区及其下属行政区序列化器"""

    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
