import os
import sys
import django
"""
自定义脚本
创建管理员账户
"""
# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Shop.settings')
django.setup()

from apps.user.models import User


def create_admin():
    admin_email = input("请输入管理员邮箱: ").strip()
    admin_name = input("请输入管理员姓名: ").strip()
    admin_password = input("请输入管理员密码: ").strip()

    # 检查邮箱是否已存在
    if User.objects.filter(email=admin_email).exists():
        print(f"错误：邮箱 {admin_email} 已存在！")
        return

    # 创建管理员
    try:
        admin_user = User.objects.create(
            email=admin_email,
            name=admin_name,
            is_staff=True,
            is_superuser=True,
        )
        admin_user.set_password(admin_password)
        admin_user.save()
        print("成功创建管理员")
        print(f"邮箱: {admin_email}")
        print(f"密码: {admin_password}")

    except Exception as e:
        print(f"创建失败: {e}")


if __name__ == "__main__":
    create_admin()