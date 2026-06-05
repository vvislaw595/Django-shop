from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
import random
import string
import re
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Django_Shop import settings
from apps.user.models import User
from apps.user.serializers import UserSerializer, UserRegisterSerializer, send_verification_email, \
    PasswordResetSerializer, ProfileSerializer, ChangePasswordSerializer
from utils import ResponseMessage
from utils.jwt_auth import create_token
from utils.password_encode import get_md5
from utils.verify_code import ImageCode


class UserAPIView(APIView):
    def post(self, request):        # 用户注册
        # 用新的注册序列化器
        # 传入request上下文用于获取Session
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # 统一错误处理
            error_message = str(e.detail) if hasattr(e, 'detail') else str(e)
            return ResponseMessage.UserResponse.error(f'注册失败: {error_message}')

        # 保存用户
        user = serializer.save()

        # 返回用户信息
        user_ser = UserSerializer(instance=user)
        return ResponseMessage.UserResponse.success({
            'user': user_ser.data,
            'message': '注册成功'
        })

    def get(self, request):
        email = request.GET.get('email')
        try:
            user_data = User.objects.get(email=email)
            # 序列化
            user_ser = UserSerializer(user_data)  # 不用加instance=user_data
            return ResponseMessage.UserResponse.success(user_ser.data)
        except Exception as e:
            print(e)
            return ResponseMessage.UserResponse.error(f'用户信息获取失败，原因：{e}')


class CaptchaAPIView(APIView):
    """生成图片验证码"""

    def get(self, request):
        image_code = ImageCode()
        captcha_text, image_base64 = image_code.get_code()

        # 将图片验证码存入Session，1分钟过期
        request.session['captcha'] = captcha_text
        request.session.set_expiry(60)
        request.session.save()

        # return ResponseMessage.UserResponse.success({
        #     'captcha_text': captcha_text,
        #     'message': '生成图片验证码成功'
        # })
        return ResponseMessage.UserResponse.success({
            'captcha_text': captcha_text,
            'image_data': f"data:image/jpeg;base64,{image_base64}",
            'message': '生成图片验证码',
        })


class EmailCodeAPIView(APIView):
    """发送邮箱验证码"""

    def post(self, request):
        email = request.data.get('email')
        captcha = request.data.get('captcha')

        if not email:
            return ResponseMessage.UserResponse.error('邮箱不能为空')

        # 更简单的邮箱验证 - 只检查是否包含@和.
        if '@' not in email or '.' not in email:
            return ResponseMessage.UserResponse.error('邮箱格式不正确')

        # 验证图片验证码 - 从Session中获取
        session_captcha = request.session.get('captcha')
        # print(session_captcha)

        if not session_captcha:
            return ResponseMessage.UserResponse.error('请先获取图片验证码')

        if session_captcha.upper() != captcha.upper():
            return ResponseMessage.UserResponse.error('图片验证码错误')

        # 检查邮箱是否已注册
        if User.objects.filter(email=email).exists():
            return ResponseMessage.UserResponse.error('该邮箱已被注册')

        # 生成6位数字验证码
        email_code = ''.join(random.choices(string.digits, k=6))

        # 将邮箱验证码存入Session，10分钟过期
        request.session[f'email_code_{email}'] = email_code
        request.session.set_expiry(600)

        # 发送邮件
        try:
            if send_verification_email(email, email_code):
                # 注意 这里不再删除图片验证码，保留到注册完成
                return ResponseMessage.UserResponse.success('验证码发送成功')
            else:
                return ResponseMessage.UserResponse.error('验证码发送失败，请稍后重试')
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return ResponseMessage.UserResponse.error('验证码发送失败，请稍后重试')


class ForgetEmailCodeAPIView(APIView):  # 忘记密码，发送邮箱验证码

    def post(self, request):
        email = request.data.get('email')
        captcha = request.data.get('captcha')

        if not email:
            return ResponseMessage.UserResponse.error('邮箱不能为空')

        # 邮箱格式验证
        if '@' not in email or '.' not in email:
            return ResponseMessage.UserResponse.error('邮箱格式不正确')

        # 验证图片验证码 - 从Session中获取
        session_captcha = request.session.get('captcha')

        if not session_captcha:
            return ResponseMessage.UserResponse.error('请先获取图片验证码')

        if session_captcha.upper() != captcha.upper():
            return ResponseMessage.UserResponse.error('图片验证码错误')

        # 检查邮箱是否注册
        if not User.objects.filter(email=email).exists():
            return ResponseMessage.UserResponse.error('该邮箱未注册')

        # 生成6位数字验证码
        email_code = ''.join(random.choices(string.digits, k=6))

        # 将邮箱验证码存入Session，10分钟过期
        # 使用不同的键名，区分注册和忘记密码
        request.session[f'forget_email_code_{email}'] = email_code
        request.session.set_expiry(600)

        # 发送邮件
        try:



            send_mail(
                subject = '密码重置验证码',
                message = f'您的密码重置验证码是：{email_code}，有效期为10分钟。',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return ResponseMessage.UserResponse.success('验证码发送成功')
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return ResponseMessage.UserResponse.error('验证码发送失败，请稍后重试')


class ResetPasswordAPIView(APIView):  # 重置密码

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            error_message = str(e.detail) if hasattr(e, 'detail') else str(e)
            return ResponseMessage.UserResponse.error(f'密码重置失败: {error_message}')

        # 重置密码
        user = serializer.save()

        return ResponseMessage.UserResponse.success({
            'message': '密码重置成功，请使用新密码登录',
            'email': user.email
        })

# 个人主页 修改信息
class UserProfileAPIView(APIView):
    def get(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)

        email = request.user.get("data").get("username")

        user = User.objects.get(email=email)
        serializer = ProfileSerializer(user)
        return ResponseMessage.UserResponse.success(serializer.data)

    def post(self, request):
        # 更新用户信息
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")

        user = User.objects.get(email=email)

        serializer = ProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return ResponseMessage.UserResponse.success({
                "message": "更新成功",
                "data": serializer.data
            })

        # 返回验证错误
        error_msg = ""
        for field, errors in serializer.errors.items():
            if errors:
                error_msg = errors[0]
                break

        return ResponseMessage.UserResponse.error(f"更新失败: {error_msg}")



# 个人主页 修改密码
class ChangePasswordAPIView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")
        user = User.objects.get(email=email)

        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            for error_list in serializer.errors.values():
                if error_list:
                    return ResponseMessage.UserResponse.error(f'验证失败，{error_list[0]}')

        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not old_password:
            return ResponseMessage.UserResponse.error("旧密码不能为空")

        # 验证旧密码是否正确
        if get_md5(old_password) != user.password:
            return ResponseMessage.UserResponse.error("旧密码错误")

        # 更新密码，这里应该是新密码，而不是旧密码
        user.password = get_md5(new_password)
        user.save()

        return ResponseMessage.UserResponse.success('密码修改成功')











class LoginView(GenericAPIView):
    def post(self, request):
        return_data = {}
        request_data = request.data
        email = request_data.get("username")
        try:
            user_data = User.objects.filter(email=email).first()
        except Exception:
            return ResponseMessage.UserResponse.other("用户名或密码错误")

        if not user_data:
            return ResponseMessage.UserResponse.other("用户名或密码错误")

        user_password = request_data.get("password")
        md5_user_password = get_md5(user_password)

        db_user_password = user_data.password

        # print(md5_user_password)
        # print(db_user_password)

        if md5_user_password != db_user_password:
            return ResponseMessage.UserResponse.other("用户名或密码错误")
        else:
            user_ser = UserSerializer(instance=user_data, many=False)
            token_info = {
                "username": email,

                # 添加user_id到token中
                "user_id": user_data.id,
                # 判断登录者是否管理员
                "is_superuser": user_data.is_superuser
            }
            token_data = create_token(token_info)
            return_data['token'] = token_data
            return_data['username'] = user_ser.data.get('name')
            return_data['is_superuser'] = user_data.is_superuser
            return ResponseMessage.UserResponse.success(return_data)





