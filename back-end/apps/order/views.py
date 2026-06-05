from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.generics import GenericAPIView

from apps.cart.models import Cart
from apps.order.models import OrderGoods, Order
from apps.order.serializers import OrderGoodsSerializer, OrderSerializer, OrderManyGoodsSerializer
from utils import ResponseMessage


class OrderGoodsGenericAPIView(GenericAPIView):
    queryset = OrderGoods.objects       # 不用.all
    serializer_class = OrderGoodsSerializer

    # 数据集合 和 序列化器
    def post(self, request):
        print(request.data)
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return JsonResponse('ok',safe=False)



    lookup_field = 'trade_no'
    # def get(self,request, trade_no):
    #     # 这行代码 查询数据库里所有数据
    #     # return JsonResponse(self.get_serializer(instance=self.get_queryset(),many=True).data,safe=False)
    #
    #
    #     # 可以查询单个 这种方式用得不多
    #     ser = self.get_serializer(instance=self.get_object(),many=False)    # 用True不行
    #     return JsonResponse(ser.data,safe=False)
    """
            33行的问题
            如果用postman获取订单商品接口，
            查询 order_goods 表里面，有两个trade_no为2的数据
            实际上这个方法只能查询一个
            所以 postman 
            用get请求 http://127.0.0.1:8000/order/goods/2 会报错
        如果你希望根据trade_no获取多个订单商品（即一个交易号对应多个订单商品），
        那么应该使用filter而不是get_object。
    """


    def get(self, request, trade_no):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")

        db_result = Order.objects.filter(email=email, is_delete=0,trade_no=trade_no).first()
            # 注意数据库里面is_delete一定要有值， =0？

        order_ser = OrderManyGoodsSerializer(instance=db_result).data
        return ResponseMessage.OrderResponse.success(order_ser)




# 获取订单
class OrderGenericAPIView(GenericAPIView):
    queryset = Order.objects
    serializer_class = OrderSerializer

    def post(self,request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")
        # 生成订单号
        import time
        trade_no = int(time.time()*1000)    # 时间戳*1000
        request_data = request.data
        trade_data = request_data["trade"]
        goods_data = request_data["goods"]
        trade_data["trade_no"] = trade_no
        trade_data["email"] = email
        trade_data["pay_status"] = 0    # 新创建的订单 支付状态=0
        trade_data["is_delete"] = 0     # 0=未删除
        trade_data["create_time"] = datetime.now()  # 不加这行，就要在models里面设置自动添加
        serializer = self.get_serializer(data=trade_data)
        # 这里应该要try
        serializer.is_valid()
        serializer.save()
        goods_order_data={}

        for data in goods_data:
            goods_order_data["trade_no"] = trade_no
            goods_order_data["sku_id"] = data["sku_id"]
            goods_order_data["goods_num"] = data.get("nums")
            if goods_order_data["goods_num"] is None:
                goods_order_data["goods_num"] = data.get("nums")
            OrderGoods.objects.create(**goods_order_data)

            # 创建完订单之后删除购物车里面的商品
            Cart.objects.filter(sku_id=data["sku_id"],email=trade_data["email"]).update(is_delete=1)

        return ResponseMessage.OrderResponse.success(serializer.data)



    def get(self,request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")
        # email = "test@qq.com"

        pay_status = request.GET.get("pay_status")
        print(pay_status)
        if pay_status == "-1":        # 查所有订单
            db_result = (Order.objects.filter(email=email,is_delete=0)
                                                .all().order_by("-create_time"))
            # 注意数据库里面is_delete一定要有值， =0？
        else:
            db_result = (Order.objects.filter(email=email, is_delete=0,
                                              pay_status=pay_status)
                                            .all().order_by("-create_time"))
        # 序列化数据
        print(db_result)
        order_ser = OrderManyGoodsSerializer(instance=db_result,many=True).data
        return ResponseMessage.OrderResponse.success(order_ser)



class OrderDetailGenericAPIView(GenericAPIView):
    queryset = Order.objects
    serializer_class = OrderSerializer

    def post(self,request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        # email = request.user.get("data").get("username")

        trade_no = request.data.get("trade_no")
        self.get_queryset().filter(trade_no=trade_no).update(**request.data)
        return ResponseMessage.OrderResponse.success("OK")



