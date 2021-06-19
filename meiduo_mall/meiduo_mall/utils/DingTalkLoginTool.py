import base64
import hmac
import logging
import time
from hashlib import sha256

from urllib.parse import urlencode, parse_qs
import json
import requests

logger = logging.getLogger('django')


class OAuthDT:
    """钉钉登陆工具类"""

    def __init__(self, appid=None, app_key=None, app_secret=None, redirect_uri=None, state=None):
        self.appid = appid
        self.redirect_uri = redirect_uri
        self.app_secret = app_secret
        self.app_key = app_key
        self.state = state

    def get_dt_url(self, loginTmpCode=None):
        """根据是否传入 loginTmpCode 返回不同阶段的url"""
        # DT登录url参数组建
        url_dict = {
            'appid': self.app_key,  # 注意这里的appid实际上需要填入appkey
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'snsapi_login',
            'state': 'STATE'
        }

        if loginTmpCode is not None:
            url_dict['loginTmpCode'] = loginTmpCode

        # 构建url
        url = 'https://oapi.dingtalk.com/connect/oauth2/sns_authorize?' + urlencode(url_dict)
        return url

    def get_unionid(self, code):
        """
        登陆钉钉后台拿用户信息(unionid)
        code是前端重回调地址中拿到的再给返回给后端
        """
        # 构造时间戳
        timestamp = str(int(round(time.time() * 1000)))
        # 构造签名
        signature = base64.b64encode(
            hmac.new(self.app_secret.encode('utf-8'), timestamp.encode('utf-8'), digestmod=sha256).digest())

        url_dict = {
            'timestamp': timestamp,
            'signature': signature,
            'accessKey': self.app_key   # 坑点，官方文档说的是appid，，巨坑
        }

        # 生成请求路径
        url = 'https://oapi.dingtalk.com/sns/getuserinfo_bycode?' + urlencode(url_dict)
        # 构造请求体
        data = {
            'tmp_auth_code': code
        }
        try:
            # 发起请求
            res = requests.post(url=url, data=json.dumps(data))
        except:
            raise Exception('获取unionid异常')

        # unionid是员工在当前开发者企业账号范围内的唯一且不变标识，由系统生成
        return json.loads(res.text).get('user_info').get('unionid')

    def get_access_token(self):
        url_dict = {
            'appkey': self.app_key,
            'appsecret': self.app_secret,
        }

        # 生成请求路径
        url = 'https://oapi.dingtalk.com/gettoken?' + urlencode(url_dict)

        try:
            # 发起请求
            res = requests.get(url=url)
        except:
            raise Exception('获取access_token异常')

        return json.loads(res.text).get('access_token')

    def get_userid(self, access_token, unionid):
        url_dict = {
            'access_token': access_token,
        }
        # 生成请求路径
        url = 'https://oapi.dingtalk.com/topapi/user/getbyunionid?' + urlencode(url_dict)
        # 构造请求体
        data = {
            'unionid': unionid
        }
        try:
            # 发起请求
            res = requests.post(url=url, data=json.dumps(data))
        except:
            raise Exception('获取userid异常')

        return json.loads(res.text).get('result').get('userid')

    def get_user_detail(self, userid, access_token, unionid):
        url_dict = {
            'access_token': access_token,
        }
        # 生成请求路径
        url = 'https://oapi.dingtalk.com/topapi/user/getbyunionid?' + urlencode(url_dict)
        # 构造请求体
        data = {
            'unionid': unionid,   # 又一个巨坑，，官方文档压根就没说要这个参数
            'userid': userid,
            'language': 'zh_CN'
        }
        try:
            # 发起请求
            res = requests.post(url=url, data=json.dumps(data))
            logger.info(res.text)
        except:
            raise Exception('获取user_detail异常')

        res_dict = json.loads(res.text)

        data = {
            # 为了和QQ保持一致，这里将unionid作为opened
            'openid': unionid,
            'userid': res_dict.get('result').get('userid'),
        }

        return data
