from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # 编辑地址标题
    path('goods_channel/', views.GoodsChannelView.as_view()),

    # 获取sku列表
    re_path('^sku_list/(?P<pk>\d+)/skus/$', views.SKUListView.as_view()),

    # 获取sku列表
    re_path('^sku_list/(?P<pk>\d+)/tops/$', views.SKUTopListView.as_view()),

    # 获取sku列表
    re_path('^sku_detail/(?P<sku_id>\d+)/$', views.SKUDetailView.as_view()),
]


router = DefaultRouter()
router.register('skus/search', views.SKUSearchViewSet, basename='skus_search')

urlpatterns += router.urls

