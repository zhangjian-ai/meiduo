import pickle, base64
from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, user, response):
    """
    本方法传入的三个参数都是对象引用，对引用的修改，本质上是对对象实力的修改
    所以无需返回值，调用方的引用指向的是已经修改的实例
    :param request: 请求对象
    :param user: user对象
    :param response: 响应对象
    :return:
    """

    # 获取前端传过来的cookie
    cookie = request.COOKIES.get('cart')

    # 如果没有cookie，则后续逻辑不需要再走
    if cookie is None:
        return

    cart = pickle.loads(base64.b64decode(cookie.encode()))
    redis_conn = get_redis_connection('cart')

    for key, value in cart.items():
        # 如果redis里面有该规格的商品，则直接覆盖，如果没有就是新增
        redis_conn.hset('cart_%d' % user.id, key, value)

    # 删除cookie
    response.delete_cookie('cart')
