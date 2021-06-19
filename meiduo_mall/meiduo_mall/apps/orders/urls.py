from django.urls import path, include, re_path

from . import views

urlpatterns = [
    # 订单结算
    path('settlement/', views.SKUSettlementView.as_view()),

    # 提交订单
    path('submit/', views.CommitOrderView.as_view()),

    # 订单列表
    path('list/', views.OrderListView.as_view()),

    # 单条订单
    re_path('retrieve/(?P<order_id>\d+)/', views.OrderRetrieveView.as_view()),

]


