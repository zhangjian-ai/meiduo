from rest_framework.pagination import PageNumberPagination


class SetPagination(PageNumberPagination):
    """
    自定义后端分页处理类，需要在settings中覆盖默认分页处理类（全局）
    非全局时，要在需要分页的视图类中指定当前类
    """
    # 使用当前类，前端需要传入当前页码page 和 每页的数量 page_size

    page_size_query_param = 'page_size'  # 设置每页数量
    max_page_size = 100  # 设置每页最大数量
    # page_query_param = 'page'  # 前端发送的页数关键字名，默认为"page"，所以无需设置
