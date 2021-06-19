from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework.filters import OrderingFilter

from .models import GoodsCategory, GoodsChannel, SKU
from .serializers import GoodsChannelSerializer, GoodsCategorySerializer, SKUListSerializer, SKUImagesSerializer, \
    GoodsDetailSerializer, SKUIndexSerializer
from collections import OrderedDict


class GoodsChannelView(APIView):
    """商品频道信息"""

    @cache_response(timeout=24 * 60 * 60, cache="home_category")
    def get(self, request):
        # 创建一个有序字典
        categories = OrderedDict()

        instance = GoodsChannel.objects.all()
        serializer = GoodsChannelSerializer(instance, many=True)

        for sub_instance, channel_data in zip(instance, serializer.data):
            group_id = sub_instance.group_id  # 当前组

            if group_id not in categories:
                categories[group_id] = {'channels': [], 'sub_cats': []}

            # 将当前频道写到对应的组内
            categories[group_id]['channels'].append(channel_data)

            # 拿到一级分类对象
            cat1 = sub_instance.category

            # 拿到当前一级分类对应的所有二级分类对象
            cat2_instance = cat1.goodscategory_set.all()

            cat2_serializer = GoodsCategorySerializer(cat2_instance, many=True)

            for cat2, cat2_channel_data in zip(cat2_instance, cat2_serializer.data):
                # 给二级分类增加一个子类，用来放三级分类
                cat2_channel_data['sub_cats'] = []

                # 拿到当前二级分类对应的所有三级分类对象
                cat3_instance = cat2.goodscategory_set.all()
                cat3_serializer = GoodsCategorySerializer(cat3_instance, many=True)

                for cat3_channel_data in cat3_serializer.data:
                    # 把三级分类名称加到二级分类的子类中
                    cat2_channel_data['sub_cats'].append(cat3_channel_data)
                categories[group_id]['sub_cats'].append(cat2_channel_data)

        category_list = []
        for value in categories.values():
            category_list.append(value)

        return Response({
            'data': category_list
        })


class SKUListView(ListAPIView):
    """此处查询sku详情，是一个标准的查所有，所以直接继承ListAPIView， 内部已经实现查询方法"""

    # 指定序列化器。 此处由于查询集需要过滤，所以不直接指定，通过重写get_quryset来提供查询集
    serializer_class = SKUListSerializer

    # 排序
    filter_backends = [OrderingFilter, ]  # 指定过滤后端排序类
    ordering_fields = ('create_time', 'price', 'sales')  # 指定可以进行排序的字段

    def get_queryset(self):
        category_id = self.kwargs['pk']  # url路径参数，在as_view()方法中（实际是继承django的View）存到了kwargs关键字参数中
        return SKU.objects.filter(is_launched=True, category_id=category_id)


class SKUTopListView(ListAPIView):
    """此处查询sku详情，是一个标准的查所有，所以直接继承ListAPIView， 内部已经实现查询方法"""

    # 指定序列化器。 此处由于查询集需要过滤，所以不直接指定，通过重写get_quryset来提供查询集
    serializer_class = SKUListSerializer

    # # 排序
    # filter_backends = [OrderingFilter, ]  # 指定过滤后端排序类
    # ordering_fields = ('sales',)  # 指定可以进行排序的字段
    def get_queryset(self):
        # url路径参数，在as_view()方法中（实际是继承django的View）存到了kwargs关键字参数中
        # 后续再通过dispatch分发给了各个方法
        category_id = self.kwargs['pk']
        res = SKU.objects.filter(is_launched=True, category_id=category_id).order_by('-sales')[:2]
        return res


class SKUDetailView(APIView):
    """获取sku详情"""

    def get(self, request, sku_id):
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return Response({'msg': 'sku不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 获取sku当前表的信息
            sku_serializer = SKUListSerializer(sku)
            sku_data = sku_serializer.data

            # 获取sku的图片
            images = sku.skuimage_set.all()
            image_serializer = SKUImagesSerializer(images, many=True)

            # Image类型的字段，不能直接获取字段的值，必须要进行序列化处理
            # for image in images_list:
            #     images_list.append(image[0].image)

            sku_data['images'] = image_serializer.data

            # 获取sku介绍信息
            desc = sku.goods
            desc_serializer = GoodsDetailSerializer(desc)

            sku_data['desc'] = desc_serializer.data

            # 获取sku规格
            sku_specs = sku.skuspecification_set.all()
            specs_list = []
            for sku_spec in sku_specs:
                # 获取商品规格对象
                goods_spec = sku_spec.spec

                # 获取规格名称
                name = goods_spec.name

                # 获取规格的值
                options = goods_spec.specificationoption_set.all()
                options_list = []
                for option in options:
                    options_list.append(option.value)

                specs_list.append({'name': name, 'list': options_list})

            sku_data['specs'] = specs_list

            return JsonResponse(sku_data)


from drf_haystack.viewsets import HaystackViewSet


class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]

    serializer_class = SKUIndexSerializer
