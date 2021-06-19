from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    path('users/', views.CreateUserView.as_view()),  # 创建用户视图
    re_path('users/(?P<username>[a-zA-Z]{3,24})/count/', views.UsernameCountView.as_view()),  # 检查用户名
    re_path('users/(?P<mobile>1[3-9]{1}[0-9]{9})/count/', views.MobileCountView.as_view()),  # 检查手机号

    # # JWT提供了登录签发JWT的视图，可以直接使用, post方法
    # path('login/', obtain_jwt_token),
    # 指定为重写后的post
    path('login/', views.UserAuthorizeView.as_view()),

    # 获取用户详情
    path('user/', views.UserDetailView.as_view()),
    # 绑定邮箱
    path('email/', views.EmailView.as_view()),
    # 绑定邮箱
    path('verify_email/', views.VerifyEmailView.as_view()),
    # 收货地址
    path('address/', views.AddressView.as_view()),
    # 编辑地址标题
    path('edit_address_title/', views.AddressTitleView.as_view()),
    # 保存浏览记录
    path('set_history/', views.UserBrowsingHistoryView.as_view())
]


