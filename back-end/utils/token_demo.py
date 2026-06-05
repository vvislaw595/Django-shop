# pip install pyjwt
import datetime

import jwt

from Django_Shop.settings import SECRET_KEY

# 自定义一个salt
SALT = '114514nbqizpdakli'
# 或者直接用Django的secret key当盐
# SECRET_KEY


def create_token():
    headers = {
        'alg': 'HS256',
        'typ': 'JWT',

    }

    payload = {
        'user_id':1,
        'username':'weiwei',
        'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=1), # 定义超时时间
    }

    result = jwt.encode(headers=headers, payload=payload, key=SECRET_KEY, algorithm='HS256')
    return result

def get_payload(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        print('token认证失败')
    except jwt.exceptions.ExpiredSignatureError:
        print('token过期')
    except jwt.exceptions.InvalidToken:
        print('无效的token')

if __name__ == '__main__':
    # token = create_token()
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IndlaXdlaSIsImV4cCI6MTc2MzQ3MzEyN30.ML2QJ5YEmb5-fmgR9cTqZxHy34ix_eF4tznGCC8dImc"
    print(token)

    payload = get_payload(token)
    print(payload)





