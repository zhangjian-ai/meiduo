import os

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from meiduo_mall.utils.alipay import FixedAliPay as AliPay
from orders.models import OrderInfo
from .models import Payment
from .keys import keys

# 构建支付对象
alipay = AliPay(
    appid=settings.ALIPAY_APPID,
    app_notify_url=None,  # 默认回调url
    app_private_key_string=keys.app_private_key_string,
    alipay_public_key_string=keys.alipay_public_key_string,
    sign_type='RSA2',
    debug=settings.ALIPAY_DEBUG  # 默认值是false
)


class PaymentView(APIView):
    """
    支付视图
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        # 校验订单
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=request.user,
                                          pay_method=OrderInfo.PAY_METHODS_ENUM['ALIPAY'],
                                          status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return Response({'msg': '订单信息有误'}, status=status.HTTP_400_BAD_REQUEST)

        # 构建链接参数
        params = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=int(order.total_amount),  # 数据库保存的是Decimal格式
            subject="美多商城：%s" % order_id,
            return_url="http://www.meiduo.site:8080/verify_order",  # 回调的web地址
        )

        # 拼接支付请求地址
        alipay_url = settings.ALIPAY_URL + "?" + params

        return Response({'url': alipay_url})


class PaymentStatusView(APIView):
    """验证支付结果"""

    def put(self, request):
        # 获取前端参数
        data = request.query_params.dict()
        signature = data.pop('sign')

        success = alipay.verify(data, signature)

        if success:
            # 获取订单号和支付流水号
            order_id = data['out_trade_no']
            trade_id = data['trade_no']

            # 新增支付记录
            Payment.objects.create(order_id=order_id, trade_id=trade_id)

            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                status=OrderInfo.ORDER_STATUS_ENUM['UNSEND'])

            return Response({'trade_id': trade_id, 'order_id': order_id})

        else:
            return Response({'msg': '请求非法'}, status=status.HTTP_403_FORBIDDEN)
