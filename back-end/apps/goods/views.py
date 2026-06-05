import decimal
import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.views import APIView

from apps.goods.models import Goods, DecimalEncoder
from apps.goods.serializers import GoodsSerializer
from utils import ResponseMessage


# 获取商品分类的接口
# 访问地址 http://localhost:8000/goods/category/1

class GoodsCategoryAPIView(APIView):
    def get(self, request, category_id, page):
        # if not request.user.get("status"):
        #     return JsonResponse(request.user,safe=False)
        current_page = (page - 1) * 20
        end_data = page * 20
        category_data = Goods.objects.filter(
            type_id = category_id).all()[current_page:end_data]

        result_list = []
        for m in category_data:
            result_list.append(m.__str__())     # 这里是字符串
        return ResponseMessage.GoodsResponse.success(result_list)


class GoodsDetailAPIView(APIView):
    def get(self, request, sku_id):
        print(sku_id)
        goods_data = Goods.objects.filter(
            sku_id = sku_id
        ).first()

        # 序列化， 序列化参数是instance， 反序列化是data
        # 所谓序列化 就是 对象变json
        # 反序列化 就是 json变对象
        result = GoodsSerializer(instance=goods_data)

        return ResponseMessage.GoodsResponse.success(result.data)


class GoodsFindAPIView(APIView):
    def get(self, request):
        goods_data = Goods.objects.filter(find=1).all()
        result = GoodsSerializer(instance=goods_data,many=True)
        return ResponseMessage.GoodsResponse.success(result.data)

class GoodsSearchAPIView(APIView):
    def get(self, request, keyword, page, order_by):
        """
        原生sql,goods是g,那一大串选出来的是r

        SELECT r.comment_count, g.image,g.name,g.p_price,g.shop_name,g.sku_id FROM goods g
        left JOIN
        (
        SELECT count(c.sku_id) as comment_count, c.sku_id from comment c GROUP BY c.sku_id
        )r
        on g.sku_id=r.sku_id
        where g.name like "%手机%"
        ORDER BY r.comment_count DESC LIMIT 10,10
        """
        order_dict = {          # 3按评论数排序，2按价格排序
                                # 1综合 评论数+价格 64开
            3:"r.comment_count",
            2:"g.p_price",
            1: "(r.comment_count)*0.6 + (g.p_price)*0.4",
        }
        limit_page = (page - 1) * 10
        # 执行原生sql
        from django.db import connection
        from django.conf import settings

        sql = """
        SELECT r.comment_count,concat('{}', g.image) as image, g.name,g.p_price,g.shop_name,g.sku_id FROM goods g
        left JOIN
        (
        SELECT count(c.sku_id) as comment_count, c.sku_id from comment c GROUP BY c.sku_id
        )r 
        on g.sku_id=r.sku_id
        where g.name like "%{}%"
        ORDER BY {} DESC LIMIT {},15
        """.format(settings.IMAGE_URL, keyword, order_dict[order_by], limit_page)

        cursor = connection.cursor()
        cursor.execute(sql)
        res  = self.dict_fetchall(cursor)
        final_list = []
        for i in res:
            res_json = json.dumps(i,cls=DecimalEncoder,ensure_ascii=False)
            final_list.append(res_json)
        return ResponseMessage.GoodsResponse.success(final_list)


    def dict_fetchall(self, cursor):
        desc = cursor.description
        # 列表推导式得到json
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")



class GoodsSearchDataCountAPIView(APIView):
    def get(self, request, keyword):
        count = Goods.objects.filter(name__contains=keyword).count()
        return HttpResponse(count)





