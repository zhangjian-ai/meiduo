from django.urls import path, include, re_path
from . import views
from . import views

urlpatterns = [
    # qq登陆界面
    path('qq/authorization/', views.QQAuthURLView.as_view()),
    # QQ登陆
    path('qq/user/', views.QQAuthUserView.as_view()),
    # 钉钉登陆二维码
    path('dt/authorization/', views.DTAuthUserView.as_view()),
    # 钉钉登陆绑定
    path('dt/user/', views.DTAuthBindUserView.as_view())
]


