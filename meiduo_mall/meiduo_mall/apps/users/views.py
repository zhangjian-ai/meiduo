from django.http import JsonResponse
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import User, Address
from meiduo_mall.libs import constants
from goods.models import SKU


class CreateUserView(CreateAPIView):
    """
    用户注册
    """
    # 指定序列化器
    serializer_class = CreateUserSerializer

    # def post(self, request, *args, **kwargs):
    #     data = super.post(request, *args, **kwargs).get('data')
    #     return JsonResponse({"code": 0, "data": data})


class UsernameCountView(APIView):
    """检查用户名是否存在"""

    def get(self, request, username):
        count = User.objects.filter(username=username).count()

        data = {
            "count": count
        }

        return Response(data)


class MobileCountView(APIView):
    """检查手机号是否存在"""

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()

        data = {
            "count": count
        }

        return Response(data)


class UserDetailView(RetrieveAPIView):
    """用户详情就是查找单一数据，直接继承RetrieveAPIView，其内部已经实现了get方法"""

    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]  # 指定权限，只有通过认证的用户才能访问当前视图

    # 如果指定了查询集，父类的get方法，通过self.get_object()获取到模型对象，然后传入序列化器进行序列化
    # 此处没有指定查询集，那么get_object()是拿不到模型对象的，没办法进行序列化
    # 但是此处是查单一，get方法父类又已经实现，如果为了request而重写get方法，那此处继承就没有意义了，而且请求参数还必须携带id或mobile才能得到模型对象
    # 此处是通过认证才能访问，那么request对象中的user对象就直接可以使用，作为序列化器的instance
    # 所以这里直接重写get_object()方法，返回用户模型对象
    def get_object(self):
        return self.request.user


class EmailView(UpdateAPIView):
    """父类中已实现put方法，修改邮箱之后，序列化器中默认发送验证邮件"""
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class VerifyEmailView(APIView):
    """邮箱验证"""

    def get(self, request):
        # 获取前端返回的token
        token = request.query_params.get('token')

        if token is None:
            return Response({'msg': '缺少token信息'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证token
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'msg': '无效的token或已经过期'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.email_active = True
            user.save()
            return Response({'msg': '验证成功'})


class AddressView(APIView):
    """增删改查地址"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = self.request.user
            instance = user.address.filter(is_deleted=False)
        except Address.DoesNotExist:
            return Response({'msg': '用户信息错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if instance.count() == 0:
                return Response({'msg': '您还添加收货地址'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserAddressSerializer(instance, many=True)
            return Response({
                'limit': constants.USER_MAX_ADDRESS_COUNT,
                'address': serializer.data
            })

    def post(self, request):
        data = request.data
        user = self.request.user
        if user.address.filter(is_deleted=False).count() < constants.USER_MAX_ADDRESS_COUNT:
            # 默认title就是收货人
            data['title'] = data.get('receiver')
            # 由于序列化器没有user字段，这里通过context传参过去，在序列化器中增加user字段
            serializer = UserAddressSerializer(data=data, context=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg': '新增地址成功'})
        else:
            return Response({'msg': '地址数量上限'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        is_default = data.get('is_default', '')

        if is_default:
            try:
                # 修改当前地址为默认地址
                instance = Address.objects.get(id=data.get('id'))

            except Address.DoesNotExist:
                return Response({'msg': '地址信息错误'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    # 先把原来的该用户下所有地址都重置为不是默认地址
                    user = self.request.user
                    all = user.address.get(is_default=True, is_deleted=False)
                except Address.DoesNotExist:
                    pass
                else:
                    all.is_default = False
                    all.save()
                finally:
                    instance.is_default = True
                    instance.save()
                    return Response({'msg': '默认地址设置成功'})
        else:
            try:
                instance = Address.objects.get(id=data.get('id'))
            except Address.DoesNotExist:
                return Response({'msg': '用户信息错误'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = UserAddressSerializer(instance, data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'msg': '修改地址成功'})

    def delete(self, request):
        data = request.data
        try:
            instance = Address.objects.get(id=data.get('id'))
        except Address.DoesNotExist:
            return Response({'msg': '地址信息错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            instance.is_deleted = True
            instance.save()
            return Response({'msg': '删除地址成功'})


class AddressTitleView(APIView):
    """修改标题"""

    def put(self, request):
        data = request.data
        try:
            instance = Address.objects.get(id=data.pop('id'))
        except Address.DoesNotExist:
            return Response({'msg': '用户信息错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = EditAddressTitleSerializer(instance, data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg': '修改地址成功'})


class UserBrowsingHistoryView(CreateAPIView):
    """
    保存浏览记录视图，直接继承，并将主要逻辑放在序列化器中
    父类已经实现新增的post方法，，，此处直接使用，无需重写
    父类CreateView中只有post，并没有get，这里我们可以自己写一个获取历史记录的get,少写一个路由
    """

    serializer_class = UserBrowsingHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取user_id
        user_id = request.user.id

        # 获取redis数据
        redis_con = get_redis_connection('history')
        history = redis_con.lrange('history_%s' % user_id, 0, -1)

        sku_list = []

        # 为了保证查询结果和列表顺序一致，这里采用循环查询
        for sku_id in history:
            sku = SKU.objects.get(id=sku_id.decode())
            sku_list.append(sku)

        serializer = SKUSerializer(sku_list, many=True)

        return Response(serializer.data)


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
from datetime import datetime
from rest_framework_jwt.views import ObtainJSONWebToken
from carts.utils import merge_cart_cookie_to_redis


class UserAuthorizeView(ObtainJSONWebToken):
    """
    重写父类的post方法，增加合并购物车cookie的逻辑
    需要修改当初的路由  2021.06.13
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            # 合并购物车
            merge_cart_cookie_to_redis(request, user, response)
            return response
