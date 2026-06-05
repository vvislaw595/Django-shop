from django.http import HttpResponse, JsonResponse
import json

class MenuResponse():
    @staticmethod
    def success(data):
        result = {"status": 200, "data": data}
        return HttpResponse(json.dumps(result), content_type = "application/json")


    @staticmethod
    def error(data):
        result = {"status": 400, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @staticmethod
    def other(data):
        result = {"status": 500, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")


############################################

# 商品的响应
class GoodsResponse():
    @staticmethod
    def success(data):
        result = {"status": 200, "data": data}
        return HttpResponse(json.dumps(result), content_type = "application/json")


    @staticmethod
    def error(data):
        result = {"status": 400, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")

    @staticmethod
    def other(data):
        result = {"status": 500, "data": data}
        return HttpResponse(json.dumps(result), content_type="application/json")


############################################

# 购物车的响应
class CartsResponse():
    @staticmethod
    def success(data):
        result = {"status": 200, "data": data}
        return JsonResponse(result,safe=False)


    @staticmethod
    def error(data):
        result = {"status": 400, "data": data}
        return JsonResponse(result,safe=False)

    @staticmethod
    def other(data):
        result = {"status": 500, "data": data}
        return JsonResponse(result,safe=False)


############################################

# 用户的响应
class UserResponse():
    @staticmethod
    def success(data):
        result = {"status": 200, "data": data}
        return JsonResponse(result,safe=False)


    @staticmethod
    def error(data):
        result = {"status": 400, "data": data}
        return JsonResponse(result,safe=False)

    @staticmethod
    def other(data):
        result = {"status": 500, "data": data}
        return JsonResponse(result,safe=False)


############################################

# 评论的响应
class CommentResponse():
    @staticmethod
    def success(data):
        result = {"status": 200, "data": data}
        return JsonResponse(result,safe=False)


    @staticmethod
    def error(data):
        result = {"status": 400, "data": data}
        return JsonResponse(result,safe=False)

    @staticmethod
    def other(data):
        result = {"status": 500, "data": data}
        return JsonResponse(result,safe=False)


############################################

# 订单的响应
class OrderResponse():
    @staticmethod
    def success(data):
        result = {"status": 200, "data": data}
        return JsonResponse(result,safe=False)


    @staticmethod
    def error(data):
        result = {"status": 400, "data": data}
        return JsonResponse(result,safe=False)

    @staticmethod
    def other(data):
        result = {"status": 500, "data": data}
        return JsonResponse(result,safe=False)


############################################

# 地址的响应
class AddressResponse():
    @staticmethod
    def success(data):
        result = {"status": 200, "data": data}
        return JsonResponse(result,safe=False)


    @staticmethod
    def error(data):
        result = {"status": 400, "data": data}
        return JsonResponse(result,safe=False)

    @staticmethod
    def other(data):
        result = {"status": 500, "data": data}
        return JsonResponse(result,safe=False)