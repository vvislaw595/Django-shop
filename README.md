# Django-Shop 全栈电商项目

基于 Django + Vue 3 的前后端分离电商商城项目。

![首页示例](首页示例.png)

## 项目简介

- **后端**: Django 5.2 + Django REST Framework + MySQL
- **前端**: Vue 3 + Vite + Element Plus + Vue Router + Vuex
- **功能**: 用户注册登录、商品浏览、购物车、订单、支付、评论、地址管理

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 5.2, DRF, PyJWT, django-cors-headers, MySQL |
| 前端 | Vue 3, Vite, Element Plus, Axios, Vue Router, Vuex |
| 认证 | JWT Token 认证 |
| 支付 | 支付宝沙箱 |

## 功能模块

### 后端 Apps

| App | 功能 |
|-----|------|
| `user` | 用户注册、登录、JWT认证、密码重置 |
| `goods` | 商品列表、分类、详情 |
| `cart` | 购物车增删改查 |
| `order` | 订单创建、查询 |
| `address` | 用户收货地址管理 |
| `comment` | 商品评论 |
| `pay` | 支付宝沙箱支付集成 |
| `menu` | 商品分类菜单 |

### 前端页面

- 首页 - 轮播banner、分类导航、商品搜索
- 商品列表页 - 按关键词搜索、排序分页
- 商品详情页 - 商品信息、评论列表、加入购物车
- 登录/注册/忘记密码
- 购物车页
- 订单页 - 确认订单、支付
- 个人中心 - 基本信息、地址管理、我的订单、安全设置

## 本地开发运行

### 环境要求

- Python 3.10+
- Node.js 20+
- MySQL 8.0+

### 1. 克隆项目

```bash
git clone git@github.com:vvislaw595/Django-shop.git
cd Django-shop
```

### 2. 后端配置

```bash
cd back-end

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install django djangorestframework pyjwt django-cors-headers mysqlclient python-alipay-sdk

# 导入数据库
# 先在MySQL创建数据库 `shop`
mysql -u root -p shop < ../../shop_fixed.sql

# 解压商品图片
# back-end/static/product_images/product_images.zip 解压到当前目录

# 运行迁移
python manage.py migrate

# 创建超级管理员
python create_admin.py

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

后端服务运行在 `http://localhost:8000`

### 3. 前端配置

```bash
cd ../front-end

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务运行在 `http://localhost:5173`

### 4. 访问

打开浏览器访问: `http://localhost:5173`

## 项目结构

```
Django-shop/
├── back-end/                # Django后端
│   ├── Django_Shop/         # 项目配置
│   │   ├── SETTINGS/         # 多环境配置
│   │   ├── settings.py       # 主配置
│   │   └── urls.py           # 路由
│   ├── apps/                 # 应用
│   │   ├── user/             # 用户模块
│   │   ├── goods/            # 商品模块
│   │   ├── cart/             # 购物车
│   │   ├── order/            # 订单
│   │   ├── address/          # 地址
│   │   ├── comment/          # 评论
│   │   └── pay/              # 支付
│   ├── static/               # 静态文件
│   │   └── product_images/   # 商品图片 (zip压缩包)
│   ├── utils/                # 工具类 (JWT认证、验证码等)
│   ├── manage.py
│   └── create_admin.py       # 创建管理员脚本
├── front-end/                # Vue3前端
│   ├── src/
│   │   ├── assets/           # 静态资源
│   │   ├── components/       # 公共组件
│   │   ├── network/          # API请求封装
│   │   ├── router/           # 路由
│   │   ├── store/            # Vuex状态管理
│   │   ├── views/            # 页面
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── shop-2026-06-03.sql      # MySQL数据库备份
```

## 默认配置

- 数据库: `shop`，用户名 `root`，密码 `123456`
- 支付宝: 使用沙箱环境，APPID 已配置
- 跨域: CORS 已开启允许所有来源

## 解压商品图片

```bash
# Windows
# 手动解压 back-end/static/product_images/product_images.zip
# 解压后: back-end/static/product_images/ 目录下会有 553 张 .jpg 图片
```

## 开发须知

- 前端开发环境通过 Vite 代理转发 `/api` 请求到后端 Django
- 后端默认 DEBUG = True，开发环境可用
- JWT Token 默认有效期 10000 分钟

## 默认账户

导入 SQL 后数据库已有数据，也可以通过 `create_admin.py` 新建管理员账户。
