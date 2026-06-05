DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shop',
        # 连接mysql
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# 静态文件服务器配置
IMAGE_URL = 'http://192.168.147.129:8000/static/product_images/'

# 支付宝沙箱
APPID="9021000158631618"

# 异步接受url post请求
APP_NOTIFY_URL="http://192.168.147.129:8000/pay/alipay/return"
# 同步        get请求
# 就是用户在页面支付成功之后 跳转到的页面
RETURN_URL="http://192.168.147.129:8000/pay/alipay/return"
# 是否开发环境
ALIPAY_DEBUG=True