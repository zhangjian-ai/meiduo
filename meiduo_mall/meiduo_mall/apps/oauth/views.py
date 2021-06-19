import logging

from django.conf import settings
from QQLoginTool.QQtool import OAuthQQ
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OAuthQQUser
from .serializers import QQAuthUserSerializer
from meiduo_mall.utils.tools import SecretTool, create_jwt_token
from meiduo_mall.utils.DingTalkLoginTool import OAuthDT
from carts.utils import merge_cart_cookie_to_redis

logger = logging.getLogger('django')


class QQAuthURLView(APIView):
    """
    返回前端QQ登陆界面的url，前端会跳转至该登陆页面
    """

    def get(self, request):
        next = request.query_params.get('next', '/')

        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)

        login_url = oauth.get_qq_url()

        return Response({'login_url': login_url})  # 返回个前端QQ登录的页面路径


class QQAuthUserView(APIView):
    """
    待用户扫码之后，QQ服务器会回调前端页面，同时传过去一个code
    当前就需要拿到code，生成access_token ,在跟去token 拿到 openid
    """

    def get(self, request):
        """根据用户是否 已绑定 返回openid或者登陆信息"""
        # 获取前端传入的code
        code = request.query_params.get('code')

        if not code:
            logger.info('缺少参数code')
            return Response({'msg': '缺少参数code'}, status=status.HTTP_400_BAD_REQUEST)

        # 床架工具对象，此处不需要state参数
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)

        # 获取access_token，，，和 openid
        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_open_id(access_token)
        except Exception:
            logger.info('QQ服务器异常')
            return Response({'msg': 'QQ服务器异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 根据openid检查该用户是否已经存在，如果存在则直接返回登陆信息，否则仅返回openid供前端绑定或注册
        try:
            qq_auth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 返回给前端的openid属于敏感信息，此处加密返回
            openid = SecretTool.encryption(openid)
            return Response({'openid': openid})
        else:
            # 如果没有异常则标识已经存在该用户，只需直接返回登陆信息
            user = qq_auth_user.user  # 通过外键拿到关联的User对象

            # 生成返回的token
            token = create_jwt_token(user)

            data = {
                'token': token,
                'id': user.id,
                'username': user.username
            }
            response = Response(data)

            # 2021.06.13  新增合并购物车cookie逻辑
            merge_cart_cookie_to_redis(request, user, response)

            return response

    def post(self, request):
        """根据用户是否存在，进行账号绑定或者新建账号"""

        # 创建序列化器
        serializer = QQAuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 执行serailizer中的各种校验
        user = serializer.save()  # save()方法就是调用create或update方法，并拿到他们的返回值再返回

        # 生成返回token
        token = create_jwt_token(user)

        response = Response({
            'token': token,
            'id': user.id,
            'username': user.username
        })

        # 2021.06.13  新增合并购物车cookie逻辑
        merge_cart_cookie_to_redis(request, user, response)

        return response


class DTAuthUserView(APIView):
    """返回登陆界面url"""

    def get(self, request):
        oauth = OAuthDT(appid=settings.DT_APP_ID, app_secret=settings.DT_CLIENT_SECRET,
                        redirect_uri=settings.DT_REDIRECT_URI, app_key=settings.DT_APP_KEY)
        loginTmpCode = request.query_params.get('loginTmpCode', '')

        url = oauth.get_dt_url()

        if loginTmpCode:
            url = oauth.get_dt_url(loginTmpCode)

        return Response({'url': url})


class DTAuthBindUserView(APIView):
    """根据钉钉用户登陆信息返回openid或者登陆信息"""

    def get(self, request):
        """根据用户是否 存在 存在则直接返回登陆信息，否则新增用户后再返回登陆信息"""
        # 获取前端传入的code
        code = request.query_params.get('code')

        if code is None:
            logger.info('缺少参数code')
            return Response({'msg': '缺少参数code'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建工具对象，此处不需要state参数
        oauth = OAuthDT(appid=settings.DT_APP_ID, app_secret=settings.DT_CLIENT_SECRET,
                        redirect_uri=settings.DT_REDIRECT_URI, app_key=settings.DT_APP_KEY)

        try:
            unionid = oauth.get_unionid(code)

            # access_token = oauth.get_access_token()
            # userid = oauth.get_userid(access_token, unionid)
            # user_detail = oauth.get_user_detail(userid, access_token, unionid)
        except Exception:
            logger.info('钉钉服务器异常')
            return Response({'msg': '钉钉服务器异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 根据openid检查关联用户是否已经存在，如果存在则直接返回登陆信息，否则调用序列化器创建关联关系
        try:
            # 钉钉登陆时，将其unionid 作为 openid 保存
            qq_auth_user = OAuthQQUser.objects.get(openid=unionid)
        except OAuthQQUser.DoesNotExist:
            # 如果不存在则反序列化创建一个用户.
            # 返回给前端的openid属于敏感信息，此处加密返回
            openid = SecretTool.encryption(unionid)
            return Response({'openid': openid})
        else:
            # 如果没有异常则表示已经存在关联用户，只需直接返回登陆信息
            user = qq_auth_user.user  # 通过外键拿到关联的User对象

            # 生成返回的token
            token = create_jwt_token(user)

            data = {
                'token': token,
                'id': user.id,
                'username': user.username
            }
            response = Response(data)

            # 2021.06.13  新增合并购物车cookie逻辑
            merge_cart_cookie_to_redis(request, user, response)

            return response
