import copy

from django.shortcuts import render
import pickle, base64

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from .serializers import CartSerializer, CartSKUSerializer
from meiduo_mall.libs import constants
from goods.models import SKU


class CartView(APIView):
    """购物车的增删改查"""

    # 由于本项目前端已经做了判断，所以不存在认证信息为空的情况
    # def perform_authentication(self, request):
    #     """
    #     重写父类的用户验证方法，不在进入视图前就检查JWT
    #     """
    #     pass

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data

        sku_id = valid_data.get('sku_id')
        count = valid_data.get('count')
        spec = valid_data.get('spec')

        # 新增规格校验，如果商品规格未勾选则返回无效请求
        if spec is None or spec == "":
            return Response({"msg": "请勾选商品规格"}, status=status.HTTP_400_BAD_REQUEST)

        # 判定用户是否登陆且认证通过
        try:
            user = request.user
        except:
            user = None

        response = Response(serializer.data, status=status.HTTP_201_CREATED)

        if user and user.is_authenticated:
            # 如果是登陆的正常用户则将购物车数据保存到redis
            redis_con = get_redis_connection('cart')

            # # 判断当前商品同一规格是否已经存在
            # origin_count = redis_con.hget('cart_%d' % user.id, '%s_%s' % (sku_id, spec))
            # if origin_count:
            #     count += int(origin_count)

            # 写入redis，hincrby 已经实现相同的key累加
            redis_con.hincrby('cart_%d' % user.id, '%s_%s' % (sku_id, spec), count)

            return response

        # 如果用户未登陆或者未通过认证 则存为cookie，但是用户购买的东西是敏感信息所以这里
        # 使用pickle和base64模块对数据进行处理

        # 先判断是否由已经保存的cart信息
        cart = request.COOKIES.get('cart')
        if cart:
            cart = pickle.loads(base64.b64decode(cart.encode()))
        else:
            cart = {}

        origin_count = cart.get('%s_%s' % (sku_id, spec))

        if origin_count:
            count += origin_count

        cart['%s_%s' % (sku_id, spec)] = count

        # 再将cart数据专程bytes
        cart = base64.b64encode(pickle.dumps(cart)).decode()

        # 创建响应并设置cookie
        response.set_cookie('cart', cart, max_age=constants.CART_COOKIE_EXPIRES)
        return response

    def get(self, request):
        """获取购物车信息"""

        # 判定用户是否登陆且认证通过
        try:
            user = request.user
        except:
            user = None

        # 获取sku信息并组装
        temp_id = 0
        temp_sku = ''
        sku_list = []
        if user and user.is_authenticated:
            redis_con = get_redis_connection('cart')
            redis_cart = redis_con.hgetall('cart_%d' % user.id)

            for item, num in redis_cart.items():
                item = item.decode().split('_', 1)
                sku_id = int(item[0])
                spec = item[1]
                count = int(num)

                if temp_id != sku_id:
                    temp_id = sku_id
                    temp_sku = SKU.objects.get(id=temp_id)
                else:
                    temp_sku = copy.deepcopy(temp_sku)
                temp_sku.spec = spec
                temp_sku.count = count

                sku_list.append(temp_sku)
        else:
            # 未登陆用户从cookie中获取
            cookie_cart = request.COOKIES.get('cart')
            if cookie_cart:
                # 将数据转换成字典
                cookie_cart = pickle.loads(base64.b64decode(cookie_cart.encode()))

                for item, num in cookie_cart.items():
                    item = item.split('_', 1)
                    sku_id = int(item[0])
                    spec = item[1]
                    count = int(num)

                    if temp_id != sku_id:
                        temp_id = sku_id
                        temp_sku = SKU.objects.get(id=temp_id)
                    else:
                        temp_sku = copy.deepcopy(temp_sku)
                    temp_sku.spec = spec
                    temp_sku.count = count

                    sku_list.append(temp_sku)

        serializer = CartSKUSerializer(sku_list, many=True)
        return Response(serializer.data)

    def put(self, request):
        """修改购物车数据"""
        serializer = CartSerializer(data=request.data.get('data'))
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data

        # 判定用户是否登陆且认证通过
        try:
            user = request.user
        except:
            user = None

        response = Response(serializer.data)

        if user and user.is_authenticated:
            # 如果是登陆的正常用户则将购物车数据保存到redis
            redis_con = get_redis_connection('cart')

            sku_id = valid_data.get('sku_id')
            count = valid_data.get('count')
            spec = valid_data.get('spec')

            # 写入redis，此处是修改商品的数量所以直接覆盖某个商品的值
            redis_con.hset('cart_%d' % user.id, '%s_%s' % (sku_id, spec), count)

            return response

        # 不是登陆用户就检查cookie
        cart = pickle.loads(base64.b64decode(request.COOKIES.get('cart').encode()))
        if cart:
            pass
        else:
            # 如果是未登陆用户，又没有携带cookie，那么就直接返回错误
            return Response({'msg': '缺少cookie信息，请先添加购物车再做修改'}, status=status.HTTP_400_BAD_REQUEST)

        sku_id = valid_data.get('sku_id')
        count = valid_data.get('count')
        spec = valid_data.get('spec')
        # 更新缓存
        cart['%s_%s' % (sku_id, spec)] = count

        # 将cart数据专程bytes，直接废弃掉以前的cookie，重新生成
        cart = base64.b64encode(pickle.dumps(cart)).decode()

        # 创建响应并设置cookie
        response.set_cookie('cart', cart, max_age=constants.CART_COOKIE_EXPIRES)
        return response

    def delete(self, request):
        valid_data = request.data

        sku_id = valid_data.get('id')
        spec = valid_data.get('spec')

        # 判定用户是否登陆且认证通过
        try:
            user = request.user
        except:
            user = None

        if user and user.is_authenticated:
            # 如果是登陆的正常用户则将购物车数据保存到redis
            redis_con = get_redis_connection('cart')

            # 写入redis，此处是修改商品的数量所以直接覆盖某个商品的值
            redis_con.hdel('cart_%d' % user.id, '%s_%s' % (sku_id, spec))

            return Response()

        cart = request.COOKIES.get('cart')
        if cart:
            cart = pickle.loads(base64.b64decode(cart.encode()))
        else:
            # 如果是未登陆用户，又没有携带cookie，那么就直接返回错误
            return Response({'msg': '缺少cookie信息，请先添加购物车再做修改'}, status=status.HTTP_400_BAD_REQUEST)

        # 删除cart中的某一规格sku
        cart.pop('%s_%s' % (sku_id, spec))

        # 将cart数据专程bytes，直接废弃掉以前的cookie，重新生成
        cart = base64.b64encode(pickle.dumps(cart)).decode()

        # 创建响应并设置cookie
        response = Response()
        response.set_cookie('cart', cart, max_age=constants.CART_COOKIE_EXPIRES)
        return response


class SelectedSkusView(APIView):
    """生成订单之前，redis暂时记录勾选的商品信息"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 保存之前，都先清空该用户之前的数据。这里以列表的形式保存
        skus = request.data.get('skus')
        user = request.user

        # 如果是登陆的正常用户则将购物车数据保存到redis
        redis_con = get_redis_connection('cart')

        # 先清空已有的预生成订单值
        redis_con.ltrim('%d' % user.id, 1, 0)

        # 将选中的sku写入到列表
        for sku in skus:
            redis_con.rpush('%d' % user.id, '%s_%s' % (sku['sku_id'], sku['spec']))
            # redis_con.hdel('cart_%d' % user.id, '%s_%s' % (sku['sku_id'], sku['spec']))

        return Response(skus, status=status.HTTP_201_CREATED)
        # return Response({'msg': "lalal"}, status=status.HTTP_403_FORBIDDEN)

