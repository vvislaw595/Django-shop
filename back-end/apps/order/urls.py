from django.urls import path, re_path
from .views import OrderGoodsGenericAPIView, OrderGenericAPIView, OrderDetailGenericAPIView

urlpatterns = [
    path('', OrderGenericAPIView.as_view()),
    path('goods/', OrderGoodsGenericAPIView.as_view()),
    path("update/", OrderDetailGenericAPIView.as_view()),

    # 正则表达式 匹配所有trade_no
    re_path('goods/(?P<trade_no>.*)', OrderGoodsGenericAPIView.as_view()),
]