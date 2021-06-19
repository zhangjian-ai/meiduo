import re

from django.contrib.auth.backends import ModelBackend

from .models import User


# 自定义JWT的登陆视图中生成响应数据的方法，追加id和username。
# 此函数在JWT中是作为配置项向外提供，所以重写之后，需要将该配置设置为重写之后的函数
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    在JWT中是默认传入了user对象的，所以可以直接获取他的id，username
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }


def get_user_by_account(account):
    """
    根据帐号获取user对象
    :param account: 账号，可以是用户名，也可以是手机号
    :return: User对象 或者 None
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 帐号为手机号
            user = User.objects.get(mobile=account)
        else:
            # 帐号为用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    继承并重写后端认证方法，在配置文件中修改成当前的认证类
    自定义用户名或手机号认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user
