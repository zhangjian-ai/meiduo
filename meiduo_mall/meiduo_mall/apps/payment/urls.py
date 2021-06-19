from django.urls import path, include, re_path

from . import views

urlpatterns = [
    # 支付
    re_path('order/payment/(?P<order_id>\d+)/', views.PaymentView.as_view()),
    # 支付验证
    path('order/verify/', views.PaymentStatusView.as_view()),
]


