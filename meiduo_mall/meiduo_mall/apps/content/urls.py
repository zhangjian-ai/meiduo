from django.urls import path, include, re_path

from . import views

urlpatterns = [
    # 编辑地址标题
    path('contents/', views.ContentView.as_view())
]


