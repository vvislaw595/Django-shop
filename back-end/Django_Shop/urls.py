"""
URL configuration for Django_Shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps import goods, pay
from apps.menu.views import GoodsMainMenu, GoodsSubMenu

# 这个是后台管理页面http://127.0.0.1:8000/admin/
# 右上角的“查看站点”转跳地址，默认是8000
# 现在将它改去前端5173
admin.site.site_url = 'http://localhost:5173'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('main_menu/', GoodsMainMenu.as_view(), name='main_menu'),
    path('sub_menu/', GoodsSubMenu.as_view(), name='sub_menu'),

    path('goods/', include('apps.goods.urls')),
    path('cart/', include('apps.cart.urls')),

    path('user/', include('apps.user.urls')),
    path('order/', include('apps.order.urls')),

    path('address/', include('apps.address.urls')),
    path('comment/', include('apps.comment.urls')),

    path("pay/",include('apps.pay.urls')),

]
