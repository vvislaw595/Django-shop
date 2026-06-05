from django.urls import path
from .views import CartView, CartDetailView, UpdateCartNumAPIView, CartCountAPIView, DeleteCartGoodsAPIView
from ..goods.views import GoodsCategoryAPIView

urlpatterns = [
    path('', CartView.as_view()),
    # path('', GoodsCategoryAPIView.as_view()),
    path("detail/", CartDetailView.as_view()),
    path("num/", UpdateCartNumAPIView.as_view()),
    path("count/", CartCountAPIView.as_view()),
    path("delete/", DeleteCartGoodsAPIView.as_view()),
]