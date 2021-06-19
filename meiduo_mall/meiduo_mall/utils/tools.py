
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings
from rest_framework_jwt.settings import api_settings


def create_jwt_token(user: object):
    """为用户创建一个jwt的加密token"""
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 导出payload生成函数
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 导出编码函数

    payload = jwt_payload_handler(user)  # 生成载荷payload部分，主要包含 id, username, expire, email等
    token = jwt_encode_handler(
        payload)  # 生成加密后的token。header部分自动加上，secret部分取用settings文件中的SECRET_KEY,没有则用jwt默认的secret

    return token


class SecretTool:
    """一个对敏感信息加密和解密的小工具"""

    @staticmethod
    def encryption(key):
        """返回秘闻"""
        # serializer = Serializer(秘钥, 有效期秒),利用配置文件中的密钥进行加密
        serializer = Serializer(settings.SECRET_KEY, 300)
        # serializer.dumps(数据), 返回bytes类型
        secret_str = serializer.dumps({'key': key})
        secret_str = secret_str.decode()  # 解码为字符串

        return secret_str

    @staticmethod
    def decryption(secret_str):
        """返回原文"""
        # 如果验证失败，会抛出itsdangerous.BadData异常。比如已经过期
        serializer = Serializer(settings.SECRET_KEY, 300)
        try:
            data = serializer.loads(secret_str)
        except BadData:
            return None
        return data.get('key')
