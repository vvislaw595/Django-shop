from django.urls import path
from .views import UserAPIView, LoginView, CaptchaAPIView, EmailCodeAPIView,ForgetEmailCodeAPIView,ResetPasswordAPIView, UserProfileAPIView, ChangePasswordAPIView


urlpatterns = [
    path('register/', UserAPIView.as_view()),
    path('login/', LoginView.as_view()),
    path('captcha/', CaptchaAPIView.as_view(), name='captcha'),
    path('email_code/', EmailCodeAPIView.as_view(), name='email_code'),
    path('forget_email_code/', ForgetEmailCodeAPIView.as_view(), name='forget_email_code'),
    path('reset/', ResetPasswordAPIView.as_view(), name='reset'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('change_password/', ChangePasswordAPIView.as_view(), name='change_password'),
    # path("debug_session/", DebugSessionAPIView.as_view(), name='debug_session'),
]