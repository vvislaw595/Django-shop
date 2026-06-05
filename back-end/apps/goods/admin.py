# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Goods


class GoodsAdmin(admin.ModelAdmin):

    list_display = ('name', 'p_price', 'shop_name','id', 'find')
    search_fields = ('name', )
    list_filter = ('find', )
    ordering = ('id',)

    def get_fieldsets(self, request, obj=None):
    # 字段分组
        if obj:
            # 编辑现有商品时显示的字段（4个字段）
            return (
                (_('商品名称'), {'fields': ['name']}),
                (_('商品价格'), {'fields': ['p_price']}),
                (_('商品图片'), {'fields': ['image']}),
                (_('商店名'), {'fields': ['shop_name']}),
                (_('是否发现好物'), {'fields': ['find']}),
            )
        else:
            # 添加新商品时显示的字段（所有15个字段）
            return (
                (None, {
                    'classes': ('wide',),
                    'fields': (
                        'type_id', 'name', 'sku_id', 'target_url',
                        'jd_price', 'p_price', 'image', 'shop_name', 'shop_id',
                        'spu_id', 'mk_price', 'vender_id', 'find',
                    )
                }),
            )


# 注册到Admin
admin.site.register(Goods, GoodsAdmin)