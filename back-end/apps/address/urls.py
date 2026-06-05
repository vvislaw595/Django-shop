from django.urls import path, re_path
from .views import AddressGenericAPIView, AddressListGenericAPIView, UserAddressDetailGenericAPIView, DeleteAddressAPIView

urlpatterns = [
    path('', AddressGenericAPIView.as_view()),
    path("edit",UserAddressDetailGenericAPIView.as_view()),
    path('list', AddressListGenericAPIView.as_view()),
    path('delete', DeleteAddressAPIView.as_view()),
    # 正则表达式要最后写
    re_path('(?P<pk>.*)', AddressGenericAPIView.as_view()),
]

"""     
        通用的正则表达式放在最后
        re_path('(?P<pk>.*)' 这个模式会匹配 所有 非空路径，
        包括 list，
        所以请求 /address/list 被这个正则表达式捕获了，
        而不是被 path('list', ...) 捕获。     
"""