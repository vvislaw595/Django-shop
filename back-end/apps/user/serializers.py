import datetime
import re
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.user.models import User
from utils.password_encode import get_md5


class UserSerializer(serializers.ModelSerializer):
    # email 作为用户名登录，做唯一性验证
    email = serializers.EmailField(
        required=True, allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")]
    )

    password = serializers.CharField(write_only=True)
    # birthday = serializers.DateTimeField("%Y-%m-%d %H:%M:%S")
    create_time = serializers.DateTimeField("%Y-%m-%d %H:%M:%S", required=False)

    def create(self, validated_data):
        validated_data['password'] = get_md5(validated_data['password'])
        validated_data['create_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = User.objects.create(**validated_data)
        print(validated_data)
        return result

    class Meta:
        model = User
        # fields = "__all__"
        fields = ['id', 'email', 'name', 'mobile', 'gender', 'birthday',
                  'create_time', 'password', 'is_staff', 'is_superuser', 'last_login']


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器 - 包含验证码功能"""
    # 基本字段
    email = serializers.CharField(
        required=True, allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="该邮箱已被注册")]
    )
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    mobile = serializers.CharField(
        required=True, allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="该手机号已被注册")]
    )

    # 验证码字段
    captcha = serializers.CharField(write_only=True, required=True)
    email_code = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        """验证密码"""
        if len(value) < 6:
            raise serializers.ValidationError("密码至少6个字符")
        if value in ("111111", "123456"):
            raise serializers.ValidationError("密码过于简单")
        return value

    def validate_mobile(self, value):
        """验证手机号格式"""
        # 手机号格式验证 11位数字
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号格式不正确")
        return value

    def validate(self, attrs):
        """综合验证"""
        # 验证密码确认
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "两次输入的密码不一致"})

        # 验证邮箱格式
        email = attrs.get('email')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise serializers.ValidationError({"email": "邮箱格式不正确"})

        # 验证图片验证码 - 使用Session
        captcha = attrs.get('captcha')
        request = self.context.get('request')
        if request and captcha:
            session_captcha = request.session.get('captcha')

            # print(f"DEBUG - Input Captcha: {captcha}, Session Captcha: {session_captcha}")

            if not session_captcha:
                raise serializers.ValidationError({"captcha": "图片验证码已过期"})
            if session_captcha.upper() != captcha.upper():
                raise serializers.ValidationError({"captcha": "图片验证码错误"})

        # 验证邮箱验证码 - 使用Session
        email_code = attrs.get('email_code')
        if email and email_code:
            session_email_code = request.session.get(f'email_code_{email}')

            print(f"DEBUG - Input Email Code: {email_code}, Session Email Code: {session_email_code}")

            if not session_email_code:
                raise serializers.ValidationError({"email_code": "邮箱验证码已过期"})
            if session_email_code != email_code:
                raise serializers.ValidationError({"email_code": "邮箱验证码错误"})

        return attrs

    def create(self, validated_data):
        """创建用户"""
        # 移除不需要保存的字段
        validated_data.pop('confirm_password')
        validated_data.pop('captcha')
        validated_data.pop('email_code')

        # 如果没有提供name，使用邮箱前缀作为默认用户名
        if not validated_data.get('name') and validated_data.get('email'):
            email_prefix = validated_data['email'].split('@')[0]
            validated_data['name'] = email_prefix

        # 加密密码
        validated_data['password'] = get_md5(validated_data['password'])

        # 设置创建时间
        validated_data['create_time'] = datetime.datetime.now()

        # 创建用户
        user = User.objects.create(**validated_data)

        # 清除已使用的验证码 - 从Session中删除
        request = self.context.get('request')
        if request:
            # 删除图片验证码（注册成功后删除）
            if 'captcha' in request.session:
                del request.session['captcha']

            # 删除邮箱验证码
            email = validated_data.get('email')
            if email and f'email_code_{email}' in request.session:
                del request.session[f'email_code_{email}']

        return user

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirm_password', 'mobile', 'captcha', 'email_code']


# 发送验证邮件
def send_verification_email(email, email_code):
    try:
        subject = '注册验证码'
        message = f'您的注册验证码是：{email_code}，有效期为10分钟。'

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False



# 重置密码
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    captcha = serializers.CharField(write_only=True, required=True)
    email_code = serializers.CharField(write_only=True, required=True)

    def validate_email(self, value):# 验证邮箱是否存在
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱未注册")
        return value

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("密码至少6个字符")
        return value

    def validate(self, attrs):
        # 验证密码确认
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "两次输入的密码不一致"})

        # 验证邮箱格式
        email = attrs.get('email')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise serializers.ValidationError({"email": "邮箱格式不正确"})

        # 验证图片验证码 - 从Session中获取
        captcha = attrs.get('captcha')
        request = self.context.get('request')
        if request and captcha:
            session_captcha = request.session.get('captcha')

            if not session_captcha:
                raise serializers.ValidationError({"captcha": "图片验证码已过期"})
            if session_captcha.upper() != captcha.upper():
                raise serializers.ValidationError({"captcha": "图片验证码错误"})

        # 验证邮箱验证码 - 从Session中获取
        email_code = attrs.get('email_code')
        if email and email_code:
            # 注意：这里使用不同的Session键名，区分注册和忘记密码
            session_email_code = request.session.get(f'forget_email_code_{email}')

            if not session_email_code:
                raise serializers.ValidationError({"email_code": "邮箱验证码已过期"})
            if session_email_code != email_code:
                raise serializers.ValidationError({"email_code": "邮箱验证码错误"})

        return attrs

    def save(self):# 重置密码
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        # 获取用户
        user = User.objects.get(email=email)

        # 更新密码
        user.password = get_md5(new_password)
        user.save()

        # 清除已使用的验证码
        request = self.context.get('request')
        if request:
            # 删除图片验证码
            if 'captcha' in request.session:
                del request.session['captcha']

            # 删除忘记密码的邮箱验证码
            if f'forget_email_code_{email}' in request.session:
                del request.session[f'forget_email_code_{email}']

        return user



# 个人主页 基本信息
class ProfileSerializer(serializers.ModelSerializer):
    gender = serializers.CharField()
    birthday = serializers.DateField(format="%Y-%m-%d")

    def get_gender(self, obj):  # 将数字转换为文字返回给前端
        gender_mapping = {0: '女', 1: '男', 2: '保密'}
        return gender_mapping.get(obj.gender, '保密')

    def validate(self, attrs):  # 验证昵称不能为空
        if 'name' in attrs and (not attrs['name'] or attrs['name'].strip() == ''):
            raise serializers.ValidationError({"name": "昵称不能为空"})
        return attrs

    def update(self, instance, validated_data):  # 更新用户信息
        if 'gender' in validated_data:
            gender_text = validated_data['gender']
            gender_mapping = {'女': 0, '男': 1, '保密': 2}
            validated_data['gender'] = gender_mapping.get(gender_text, 2)

        # 更新其他字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if 'gender' in ret and ret['gender'] is not None:
            gender_mapping = {0: '女', 1: '男', 2: '保密'}
            gender_num = int(ret['gender'])
            ret['gender'] = gender_mapping.get(gender_num, '保密')
        return ret

    class Meta:
        model = User
        fields = ['name', 'gender', 'birthday']


# 个人主页 修改密码
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        if not value:
            raise serializers.ValidationError("旧密码不能为空")
        return value

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("密码至少6个字符")
        if value in ("111111","123456"):
            raise serializers.ValidationError("密码过于简单")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "两次输入的密码不一致"})
        return attrs

    def save(self, user):
        new_password = self.validated_data['new_password']

        user.password = get_md5(new_password)
        user.save()
        return user
