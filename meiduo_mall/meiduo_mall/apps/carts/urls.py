from django.urls import path, include, re_path

from . import views

urlpatterns = [
    # 购物车
    path('cart/', views.CartView.as_view()),

    # 生成订单的商品
    path('selects/', views.SelectedSkusView.as_view())
]


