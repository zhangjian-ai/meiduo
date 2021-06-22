from hashlib import md5  # py3.x
import base64
import datetime
# import urllib2
import urllib.request as urllib2  # py3.x
import json
from .xmltojson import xmltojson
from xml.dom import minidom


class REST:
    AccountSid = ''
    AccountToken = ''
    AppId = ''
    SubAccountSid = ''
    SubAccountToken = ''
    ServerIP = ''
    ServerPort = ''
    SoftVersion = ''
    Batch = ''  # 时间戳
    BodyType = 'json'  # 包体格式，可填值：json 、xml

    # 初始化
    # @param serverIP       必选参数    服务器地址
    # @param serverPort     必选参数    服务器端口
    # @param softVersion    必选参数    REST版本号
    def __init__(self, ServerIP, ServerPort, SoftVersion):
        self.ServerIP = ServerIP;
        self.ServerPort = ServerPort;
        self.SoftVersion = SoftVersion;

    # 设置主帐号
    # @param AccountSid  必选参数    主帐号
    # @param AccountToken  必选参数    主帐号Token

    def setAccount(self, AccountSid, AccountToken):
        self.AccountSid = AccountSid;
        self.AccountToken = AccountToken;

    # 设置应用ID
    #
    # @param AppId  必选参数    应用ID

    def setAppId(self, AppId):
        self.AppId = AppId

    # 发送模板短信
    # @param to  必选参数     短信接收彿手机号码集合,用英文逗号分开
    # @param datas 可选参数    内容数据
    # @param tempId 必选参数    模板Id
    def sendTemplateSMS(self, to, datas, tempId):
        # self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        signature = signature.encode('utf-8')  # py3

        sig = md5(signature).hexdigest().upper()  # py3
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + self.ServerPort + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/SMS/TemplateSMS?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        # auth = base64.encodestring(src).strip()
        auth = base64.encodebytes(src.encode()).strip()
        req = urllib2.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        # 创建请求体

        # --------------这里是xml格式的请求体--------------
        # b = ''
        # for a in datas:
        #     b += '<data>%s</data>' % (a)
        #
        # body = '<?xml version="1.0" encoding="utf-8"?><SubAccount><datas>' + b + '</datas><to>%s</to><templateId>%s</templateId><appId>%s</appId>\
        #         </SubAccount>\
        #         ' % (to, tempId, self.AppId)
        # --------------这里是xml格式的请求体--------------

        if self.BodyType == 'json':
            body = '''{"to": "%s", "datas": %s, "templateId": "%s", "appId": "%s"}''' % (
            to, str(datas), tempId, self.AppId)
        req.data = body.encode()  # py3
        try:

            res = urllib2.urlopen(req)
            data = res.read()
            res.close()

            if self.BodyType == 'json':
                # json格式
                locations = json.loads(data)
            else:
                # xml格式
                xtj = xmltojson()
                locations = xtj.main(data)
            return locations
        except Exception as error:
            return {'172001': f'网络错误:{error}'}

    # 设置报头
    def setHttpHeader(self, req):
        if self.BodyType == 'json':
            req.add_header("Accept", "application/json")
            req.add_header("Content-Type", "application/json;charset=utf-8")

        else:
            req.add_header("Accept", "application/xml")
            req.add_header("Content-Type", "application/xml;charset=utf-8")
