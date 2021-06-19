from urllib.parse import quote_plus

from alipay import AliPay
import logging

logger = logging.getLogger('django')


class FixedAliPay(AliPay):
    """继承需改sign_data方法"""

    def sign_data(self, data):
        # 排序后的字符串
        ordered_items = self._ordered_data(data)
        raw_string = "&".join("{}={}".format(k, v) for k, v in ordered_items)
        sign = self._sign(raw_string)
        unquoted_items = ordered_items + [('sign', sign)]

        # 获得最终的订单信息字符串
        signed_string = "&".join("{}={}".format(k, quote_plus(str(v))) for k, v in unquoted_items)
        # signed_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in unquoted_items)
        if self._verbose:
            logger.debug("signed srtring")
            logger.debug(signed_string)
        return signed_string
