# Django-Shop 部署教程：Railway（后端 + MySQL）

## 准备工作

- GitHub 账号，仓库已推送：`https://github.com/vvislaw595/Django-shop`
- Railway 账号（用 GitHub 直接登录）

---

## 第一步：注册 Railway 并创建项目

1. 打开 https://railway.app/
2. 点击 **Login** → **Login with GitHub** 授权登录
3. 登录后进入 Dashboard，点击 **New Project**
4. 选择 **Deploy from GitHub repo**
5. 如果没有看到仓库，点击 **Configure GitHub App** 授权 Railway 访问你的仓库
6. 搜索并选择 `vvislaw595/Django-shop`

---

## 第二步：添加 MySQL 数据库

1. 在项目页面，点击右侧 **Add** 按钮
2. 选择 **Database** → **MySQL**
3. Railway 会自动创建 MySQL 实例，等待几秒完成
4. 创建完成后，点击 MySQL 卡片进入详情页

---

## 第三步：获取数据库连接信息

在 MySQL 详情页，点击 **Connect** 标签，你会看到：

```
Public Network
mysql://root:你的密码@acela.proxy.rlwy.net:端口号/railway
```

**记下这些信息：**
- Host: `acela.proxy.rlwy.net`（你的实际地址可能不同）
- Port: 端口号（如 `27595`）
- User: `root`
- Password: 密码
- Database: `railway`

> 注意：用 **Public Network** 的连接信息，`Internal Network` 只能在 Railway 内部使用。

---

## 第四步：导入数据库

### 方式一：Navicat 导入（推荐）

1. 打开 Navicat → 新建 MySQL 连接
2. 填入上面获取的 Host、Port、User、Password
3. 连接成功后，双击打开 `railway` 数据库
4. 右键 `railway` → **运行 SQL 文件**
5. 选择本地的 `shop_fixed.sql` 文件
6. 点击开始，等待导入完成

### 方式二：命令行导入

```bash
mysql -h 你的Host -u root -p --port 你的端口 --protocol=TCP railway < shop_fixed.sql
```

### 验证导入

导入后在 Navicat 中查看，应能看到以下表：

> `auth_user`、`goods`、`shopping_cart`、`order`、`order_goods`、`comment`、`user`、`user_address`、`main_menu`、`sub_menu` 等

---

## 第五步：配置环境变量

1. 回到 Railway 项目页面
2. 点击顶部的 **Variables** 标签
3. 点击 **New Variable** 逐个添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `DJANGO_SECRET_KEY` | 随机字符串 | 在 https://djecrety.ir/ 生成一个 |
| `DJANGO_DEBUG` | `False` | 生产环境关闭调试 |
| `ALLOWED_HOSTS` | `*.railway.app,localhost` | 允许访问的域名 |
| `DB_HOST` | 你的MySQL Host | 如 `acela.proxy.rlwy.net` |
| `DB_PORT` | 你的MySQL端口 | 如 `27595` |
| `DB_NAME` | `railway` | 数据库名 |
| `DB_USER` | `root` | 数据库用户名 |
| `DB_PASSWORD` | 你的MySQL密码 | 数据库密码 |

> 变量名必须和 `settings.py` 中 `os.environ.get()` 的参数名一致。

---

## 第六步：配置部署设置

1. 点击项目顶部的 **Settings**
2. 找到 **Root Directory** 设置
3. 填写：`back-end`
4. 找到 **Start Command** 设置
5. 填写以下启动命令：

```bash
cd back-end && python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT
```

6. Railway 会自动识别 `requirements.txt` 安装依赖

---

## 第七步：部署

1. 点击 **Deploy** 按钮
2. Railway 会：
   - 拉取 GitHub 代码
   - 安装 Python 依赖（`pip install -r requirements.txt`）
   - 运行数据库迁移
   - 启动 Django 服务
3. 等待构建完成，顶部会显示部署状态
4. 部署成功后，点击 **View Logs** 查看日志确认无报错

---

## 第八步：获取域名

1. 部署成功后，点击项目卡片上的 **Generate Domain**
2. Railway 会分配一个域名，格式如：
   ```
   https://django-shop-backend-production.up.railway.app
   ```
3. 复制这个域名，这是你的后端 API 地址

---

## 第九步：测试 API

在浏览器或 Postman 中访问：

```
https://你的域名/api/goods/
```

如果返回商品 JSON 数据，说明部署成功。

---

## 常见问题

### Q1: 部署失败，报错 "ModuleNotFoundError: No module named 'xxx'"
**A**: 检查 `requirements.txt` 是否包含所有依赖，确保已推送到 GitHub。

### Q2: 数据库连接失败
**A**: 检查环境变量中的 `DB_HOST` 和 `DB_PORT` 是否与 Railway 提供的 Public Network 信息一致。

### Q3: 静态文件（商品图片）404
**A**: 确保 `product_images.zip` 已解压到 `back-end/static/product_images/` 目录。

### Q4: 部署成功但访问 API 返回 500
**A**: 查看 Railway 日志，通常是数据库表未迁移或环境变量未配置。

### Q5: Railway 免费额度
**A**: 每月 $5 免费额度，包含 500 小时运行时间、1GB RAM、MySQL 免费额度。个人项目完全够用。

---

## 下一步

后端部署完成后，继续部署前端到 Vercel：

1. 修改 `front-end/.env.production` 中的 `VITE_API_BASE_URL` 为 Railway 后端域名
2. 将前端部署到 Vercel（免费）
3. 配置 CORS 允许 Vercel 域名

---

## 部署后的项目地址

| 服务 | 地址 |
|------|------|
| 后端 API | `https://你的域名.railway.app` |
| 前端页面 | Vercel 分配（下一步部署） |
| API 文档 | `https://你的域名.railway.app/api/goods/` |