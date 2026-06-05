from django.urls import path, re_path
from .views import CommentGenericAPIView, CommentAPIView, CommentCountAPIView

urlpatterns = [
    path("detail", CommentAPIView.as_view()),
    path("count", CommentCountAPIView.as_view()),

    path('', CommentGenericAPIView.as_view({
        # 不传参
        # http://127.0.0.1:8000/comment/
        "get":"my_list",        # 查询全部评论
        "post":"my_save",       # 保存评论
    })),

    re_path('(?P<pk>.*)', CommentGenericAPIView.as_view({
        # 传参 是 数字
        # http://127.0.0.1:8000/comment/参数
        "get":"single",         # 查参数的评论
        "post":"edit",           # 修改更新参数的
        "delete":"my_delete",   # 删参数的
    })),



]