from rest_framework import serializers

from Django_Shop.settings import IMAGE_URL
from apps.goods.models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    # 写的字段  就是想要序列化处理的字段
    image = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField("%Y-%m-%d %H:%M:%S")


    def get_image(self, obj):
        new_image_path = IMAGE_URL + obj.image
        return new_image_path


    class Meta:
        model = Goods
        fields = '__all__'





