# pip install pyjwt
import datetime

import jwt
from rest_framework.authentication import BaseAuthentication

from Django_Shop.settings import SECRET_KEY



def create_token(payload, timeout=10000):       # 单位 分钟
    headers = {
        'alg': 'HS256',
        'typ': 'JWT',

    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)

    result = jwt.encode(headers=headers, payload=payload, key=SECRET_KEY, algorithm='HS256')
    return result

def get_payload(token):
    result = {"status": False, "data":None, "error": None}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        result["status"] = True
        result["data"] = payload

    except jwt.exceptions.DecodeError:
        print('token认证失败')
        result["error"] = "token认证失败"
    except jwt.exceptions.ExpiredSignatureError:
        print('token失效')
        result["error"] = "token失效"
    except jwt.exceptions.InvalidToken:
        print('无效的token')
        result["error"] = "无效的token"
    return result


# 用户在url中进行token参数配置
class JwtQueryParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 从url中拿到token
        token = request.GET.get("token")
        result_payload = get_payload(token)
        print(result_payload)

        # if not result_payload["status"]:
        #     raise

        return (result_payload, token)


class JwtHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 从头信息中拿到token
        # print(request.META)
        # token = request.META.get("HTTP_TOKEN")            # postman获取
        token = request.META.get("HTTP_AUTHORIZATION")      # 浏览器获取
        # print(token)

        result_payload = get_payload(token)

        # 这行打印{'status': False, 'data': None, 'error': 'token认证失败'}
        print(result_payload)
        return (result_payload, token)
