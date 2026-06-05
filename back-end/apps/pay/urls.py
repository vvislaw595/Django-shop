from django.urls import path, re_path
from .views import ToAliPayPageAPIView, AlipayAPIView

urlpatterns = [
    path('alipay', ToAliPayPageAPIView.as_view(), name='pay'),
    path('alipay/return', AlipayAPIView.as_view(), name='alipay'),
]