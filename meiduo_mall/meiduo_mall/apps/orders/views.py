import copy

from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from .models import OrderInfo, OrderGoods
from carts.serializers import CartSKUSerializer
from .serializers import CommitOrderSerializer, OrderListSerializer


class SKUSettlementView(APIView):
    """订单结算"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        结算界面展示待生成订单的商品列表
        :param request:
        :return:
        """
        # 如果是登陆的正常用户则将购物车数据保存到redis
        redis_con = get_redis_connection('cart')
        user = request.user
        # 获取缓存的待结算的全部商品
        skus = redis_con.lrange('%d' % user.id, 0, -1)

        if skus == []:
            return Response({'msg': '无可结算商品'}, status=status.HTTP_400_BAD_REQUEST)

        temp_id = 0
        temp_sku = ''
        sku_list = []
        for sku in skus:
            sku_id, spec = sku.decode().split('_', 1)
            # 保存sku的信息
            count = redis_con.hget('cart_%d' % user.id, '%s_%s' % (sku_id, spec))

            if temp_id != sku_id:
                temp_id = sku_id
                temp_sku = SKU.objects.get(id=temp_id)
            else:
                temp_sku = copy.deepcopy(temp_sku)

            temp_sku.spec = spec
            temp_sku.count = int(count)

            sku_list.append(temp_sku)

        # 借用购物车的序列化器
        serializer = CartSKUSerializer(sku_list, many=True)

        return Response(serializer.data)


class CommitOrderView(CreateAPIView):
    """提交订单主要就是创建订单和订单详情单
    所以这里直接继承有post方法的视图类
    """
    permission_classes = [IsAuthenticated]

    # 创建数据只需要指定序列化器，创建具体逻辑都放到序列化器中
    serializer_class = CommitOrderSerializer


class OrderListView(ListAPIView):
    """查询用户全部订单"""

    permission_classes = [IsAuthenticated]

    # # 排序
    # filter_backends = [OrderingFilter, ]  # 指定过滤后端排序类
    # ordering_fields = ('status', 'create_time')  # 指定可以进行排序的字段

    serializer_class = OrderListSerializer

    def get_queryset(self):
        user = self.request.user
        order = OrderInfo.objects.filter(user=user).order_by('status', '-create_time')

        return order


class OrderRetrieveView(APIView):
    """查询单条订单"""

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = OrderInfo.objects.get(order_id=order_id)
        except OrderInfo.DoesNotExist:
            return Response({'msg': '订单号不存在'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderListSerializer(order)

        return Response(serializer.data)

