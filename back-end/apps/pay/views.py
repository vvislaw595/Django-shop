from datetime import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.views import APIView

from apps.order.models import Order
from apps.pay.alipay import Alipay

class ToAliPayPageAPIView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user,safe=False)

        trade_no = request.data.get('tradeNo')
        # 这里没写主题？看前端OrderPay 44行定义
        total_amount = request.data.get('orderAmount')

        alipay = Alipay()
        url = alipay.direct_pay(
            out_trade_no = trade_no,
            subject = "主题：" + trade_no,
            total_amount = total_amount,
        )
        # print(url)

        re_url = alipay.gateway + "?{data}".format(data=url)
        return JsonResponse({"alipay":re_url})


class AlipayAPIView(APIView):
    def get(self, request):
        processed_dict = {}

        for k,v in request.GET.items():
            processed_dict[k] = v

        sign = processed_dict.pop('sign',None)
        alipay = Alipay()
        is_verify = alipay.verify(processed_dict, sign)

        if is_verify is True:
            trade_no = processed_dict.get("out_trade_no")
            ali_trade_no = processed_dict.get("trade_no")
            pay_status = 2
            Order.objects.filter(trade_no=trade_no).update(
                ali_trade_no=ali_trade_no,
                pay_status=pay_status,
                pay_time=datetime.now())

        # 如果是False 要有提示，不能让他返回到个人页，这里没写
        return redirect("http://localhost:5173/profile?activeIndex=3")


    def post(self, request):
        processed_dict = {}

        for k, v in request.POST.items():
            processed_dict[k] = v

        sign = processed_dict.pop('sign', None)
        alipay = Alipay()
        is_verify = alipay.verify(processed_dict, sign)

        if is_verify is True:
            trade_no = processed_dict.get("out_trade_no")
            ali_trade_no = processed_dict.get("trade_no")
            # 0待支付  1 待确认  2支付完成  3 已完成
            pay_status = 2
            Order.objects.filter(trade_no=trade_no).update(
                ali_trade_no=ali_trade_no,
                pay_status=pay_status,
                pay_time=datetime.now())
        return redirect("http://localhost:5173/profile?activeIndex=3")