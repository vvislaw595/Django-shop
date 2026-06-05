from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserAddress

# Register your models here.

class UserAdmin(BaseUserAdmin):
    # 列表显示
    list_display = ('email', 'name', 'mobile', 'is_staff', 'is_superuser', 'last_login', 'create_time')
    list_filter = ('is_staff', 'is_superuser', 'gender')
    search_fields = ('email', 'name', 'mobile')
    ordering = ('-create_time',)

    # 字段分组
    fieldsets = (
        (_('账户信息'), {'fields': ('email', 'password')}),
        (_('个人信息'), {'fields': ('name', 'birthday', 'mobile', 'gender')}),
        (_('权限'), {'fields': ('is_staff', 'is_superuser')}),
    )

    # 添加用户时的字段
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    def save_model(self, request, obj, form, change):
        """保存用户时处理密码"""
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


class UserAddressAdmin(admin.ModelAdmin):
    """用户地址管理"""
    list_display = ('signer_name', 'telphone', 'district', 'default', 'create_time')
    list_filter = ('district', 'default')
    search_fields = ('email','signer_name', 'telphone')
    # raw_id_fields = ('user',)


admin.site.site_header = '商城管理系统'
admin.site.site_title = '商城管理后台'
admin.site.index_title = '商城管理系统'

# 注册到Admin
admin.site.register(User, UserAdmin)
admin.site.register(UserAddress, UserAddressAdmin)


