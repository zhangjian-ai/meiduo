from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from .models import ContentCategory
from .serializers import ContentSerializer, ContentCategorySerializer


class ContentView(APIView):
    """广告视图"""

    @cache_response(timeout=24*60*60, cache="home_content")
    def get(self, request):
        # 返回一个以广告类别为item的列表
        contents_list = []

        categories = ContentCategory.objects.all()
        serializers = ContentCategorySerializer(categories, many=True)

        for category, serializer in zip(categories, serializers.data):
            # 通过一对多关系获取广告详情内容，过滤掉不展示的广告
            contents = category.content_set.filter(status=1)
            contents_serializers = ContentSerializer(contents, many=True)

            serializer['contents'] = contents_serializers.data
            contents_list.append(serializer)

        return Response({
            'data': contents_list
        })
