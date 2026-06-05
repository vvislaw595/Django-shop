from email.headerregistry import Address

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, \
    ListModelMixin
from rest_framework.views import APIView

from apps.address.models import UserAddress
from apps.address.serializers import AddressSerializer
from utils import ResponseMessage
from utils.jwt_auth import JwtQueryParamAuthentication, JwtHeaderAuthentication


# Create your views here.


class AddressGenericAPIView(GenericAPIView, CreateModelMixin,
                            RetrieveModelMixin, UpdateModelMixin,
                            DestroyModelMixin):
    queryset = UserAddress.objects
    serializer_class = AddressSerializer
    authentication_class = [JwtHeaderAuthentication, ]

    # 增 获取 改 删
    def post(self, request):  # 新增收货地址
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")

        request_data = request.data
        request_data["email"] = email
        # 如果数据库里面这个值是1，那么就是默认地址，其他地址设为0
        if request_data["default"] == True:
            self.get_queryset().filter(email=email).update(default=0)
            request_data["default"] = 1
        else:
            request_data["default"] = 0

        self.get_queryset().create(**request_data)

        return ResponseMessage.AddressResponse.success("新增成功")

    def get(self, request):  # 返回全部地址
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")
        db_result = self.get_queryset().filter(email=email).all().order_by("-default", "create_time")
        ser = self.get_serializer(instance=db_result, many=True)
        return ResponseMessage.AddressResponse.success(ser.data)

        # return self.retrieve(request)

    # def put(self, request, pk):
    #     return self.update(request, pk)
    #
    # def delete(self, request, pk):
    #     return self.destroy(request, pk)


class AddressListGenericAPIView(GenericAPIView, ListModelMixin):
    queryset = UserAddress.objects
    serializer_class = AddressSerializer
    authentication_classes = [JwtQueryParamAuthentication, ]

    def get(self, request):
        # 拿到token返回的第一个值
        print(request.user)
        # 拿到token返回的第2个值
        print(request.auth)
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)

        return self.list(request)


class UserAddressDetailGenericAPIView(GenericAPIView, CreateModelMixin,
                                      RetrieveModelMixin, UpdateModelMixin,
                                      DestroyModelMixin):
    queryset = UserAddress.objects
    serializer_class = AddressSerializer

    def post(self, request):  # 新增收货地址
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")

        request_data = request.data
        request_data["email"] = email
        # 如果数据库里面这个值是1，那么就是默认地址，其他地址设为0
        if request_data["default"] == True:
            self.get_queryset().filter(email=email).update(default=0)
            request_data["default"] = 1
        else:
            request_data["default"] = 0
        self.get_queryset().filter(id=request_data["id"]).update(**request_data)

        return ResponseMessage.AddressResponse.success("更新成功")


class DeleteAddressAPIView(GenericAPIView):
    # authentication_classes = [JwtQueryParamAuthentication, ]
    queryset = UserAddress.objects
    serializer_class = AddressSerializer

    def post(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        from utils.jwt_auth import get_payload
        auth_result = get_payload(token)

        if not auth_result.get("status"):
            print(f"手动认证失败: {auth_result}")
        else:
            email = auth_result.get("data").get("username")
            address_id = request.data.get("id")

        address = self.get_queryset().filter(email=email, id=address_id).first()

        # 统计用户有多少个地址
        user_address_count = self.get_queryset().filter(email=email).count()
        if user_address_count == 1:  # 一个地址 直接删除
            address.delete()
            return ResponseMessage.AddressResponse.success("删除地址成功")

        if address.default == 1:
            other_address = (self.get_queryset().filter(email=email).
                             exclude(id=address_id).order_by("create_time").first())
            if other_address:
                other_address.default = 1
                other_address.save()
        address.delete()
        return ResponseMessage.AddressResponse.success("删除地址成功")
