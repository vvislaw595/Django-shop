from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from utils import ResponseMessage
from .models import Cart
from .serializers import CartSerializer, CartDetailSerializer


class CartView(APIView):
    '''
        购物车应该是登录了才能用
        后续 学习了 token 登录权限验证 再做补充
    '''

    def post(self, request):
        request_data = request.data
        print("接收到的数据:", request.data)
        # email = request_data.get('email')
        # token验证
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")
        request_data["email"] = email  # 查到email之后还要把他添加进去

        sku_id = request_data.get('sku_id')
        nums = request_data.get('nums')
        is_delete = request_data.get('is_delete')

        # 判断数据是否存在
        # 存在 更新，不存在 插入
        # data_exists = Cart.objects.filter(email=email, is_delete=0, sku_id=sku_id)

        # 修改查询条件：不限制is_delete状态，查找所有状态的记录
        data_exists = Cart.objects.filter(email=email, sku_id=sku_id).first()

        if data_exists:
            # 记录存在，无论是否删除
            if is_delete == 0:  # 添加/更新操作
                if data_exists.is_delete == 1:
                    # 如果是已删除的商品，重新激活
                    data_exists.is_delete = 0
                    data_exists.nums = nums  # 重置数量为新的数量
                    data_exists.save()
                    return ResponseMessage.CartsResponse.success("重新添加商品成功")
                else:
                    # 如果是未删除的商品，更新数量
                    new_nums = nums + data_exists.nums
                    data_exists.nums = new_nums
                    data_exists.save()
                    return ResponseMessage.CartsResponse.success("更新商品数量成功")
            elif is_delete == 1:  # 删除操作
                if data_exists.is_delete == 0:
                    data_exists.is_delete = 1
                    data_exists.save()
                    return ResponseMessage.CartsResponse.success("成功将商品移出购物车")
                else:
                    return ResponseMessage.CartsResponse.success("商品已在删除状态")
        else:
            # 记录不存在，创建新记录
            if is_delete == 1:
                return ResponseMessage.CartsResponse.success("成功将商品加从删除购物车")

            cart_ser = CartSerializer(data=request_data)
            cart_ser.is_valid(raise_exception=True)
            Cart.objects.create(**cart_ser.data)
            return ResponseMessage.CartsResponse.success("成功将商品加入购物车")

    def get(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.GET.get("email")
        cart_result = Cart.objects.filter(email=email, is_delete=0)
        cart_ser = CartSerializer(instance=cart_result, many=True)
        return ResponseMessage.CartsResponse.success(cart_ser.data)


# 用序列化器，多表查询
class CartDetailView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")  # 获取登录的用户
        filter = {
            "email": email,
            "is_delete": 0,
        }
        shopping_cart = Cart.objects.filter(**filter).all()
        db_data = CartDetailSerializer(shopping_cart, many=True).data
        return ResponseMessage.CartsResponse.success(db_data)


class UpdateCartNumAPIView(APIView):
    def post(self, request):  # 从token获取email
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)

        print(request.user)
        email = request.user.get("data").get("username")  # 获取登录的用户
        request_data = request.data
        Cart.objects.filter(
            email=email,
            sku_id=request_data["sku_id"],
            is_delete=0,
        ).update(nums=request_data["nums"])
        return ResponseMessage.CartsResponse.success("ok")


class DeleteCartGoodsAPIView(APIView):
    def post(self, request):  # 从token获取email
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)

        print(request.user)
        email = request.user.get("data").get("username")  # 获取登录的用户
        request_data = request.data
        Cart.objects.filter(
            email=email,
            sku_id__in=request_data,
            is_delete=0,
        ).update(is_delete=1)
        return ResponseMessage.CartsResponse.success("ok")


# 获取购物车商品数量
class CartCountAPIView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        print(request.user)
        email = request.user.get("data").get("username")
        user_cart_count = Cart.objects.filter(email=email,
                                              is_delete=0,
                                              ).aggregate(Sum('nums'))
        return ResponseMessage.CartsResponse.success(user_cart_count)
