# Clean Creation MVP

第一版 MVP：Vue 3 + Vite 前端、Django 后端、TiDB Cloud 可配置、mock 支付、积分计费、上传、任务、后台。

## 本地启动

后端：

```bash
cd /Volumes/D/个人网站
source venv/bin/activate
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

前端：

```bash
cd /Volumes/D/个人网站/frontend
npm install
npm run dev -- --host 127.0.0.1
```

访问：

```text
http://127.0.0.1:5173/
```

## TiDB 环境变量

真实值只放后端环境变量，不写入代码：

```env
DATABASE_HOST=
DATABASE_PORT=4000
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_SSL=true
JWT_SECRET=
CREDIT_RATE=10
MAX_UPLOAD_MB=5
ENABLE_FFMPEG=false
```

未配置 `DATABASE_HOST` 时，本地自动使用现有 SQLite，方便免费开发。

## Render 后端部署

- Root Directory: 项目根目录 `个人网站`
- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start Command: `gunicorn personal_site.wsgi:application --bind 0.0.0.0:$PORT`
- Plan: Free
- 设置 `.env.example` 中的后端环境变量
- `CORS_ALLOWED_ORIGINS` 填前端正式域名

## Vercel / Cloudflare Pages 前端部署

- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `dist`
- 环境变量：`VITE_API_BASE_URL=https://你的-render-api域名/api`

`frontend/vercel.json` 和 `frontend/public/_redirects` 已处理 SPA 路由回退。

## 已实现

- 注册：`POST /api/auth/register`
- 登录：`POST /api/auth/login`
- 当前用户和积分：`GET /api/auth/me`
- 积分钱包：`GET /api/wallet`
- 积分流水：`GET /api/credits/ledger`
- 创建订单：`POST /api/orders/create`
- 订单列表：`GET /api/orders`
- 订单详情：`GET /api/orders/:id`
- mock 支付成功：`POST /api/payments/mock/pay`
- 上传文件：`POST /api/files/upload`
- 文件列表：`GET /api/files`
- 创建处理任务：`POST /api/jobs/create`
- 任务列表：`GET /api/jobs`
- 任务详情：`GET /api/jobs/:id`
- 管理后台汇总：`GET /api/admin/overview`
- 管理员调整积分：`POST /api/admin/credits/adjust`

## 新增表

- `credit_wallets`
- `credit_ledger`
- `orders`
- `files`
- `processing_jobs`
- `social_accounts`
- `publish_jobs`

Django 实际表名带 app 前缀，例如 `website_creditwallet`。

## 测试闭环

1. 注册：打开 `/signup`，输入邮箱/手机号和密码。
2. 登录：打开 `/login`，登录后进入 `/dashboard`。
3. 充值：打开 `/recharge`，选择套餐并 mock 支付。
4. 积分增加：用户中心或 `/credits` 查看余额和 `recharge` 流水。
5. 上传小图片：打开 `/upload`，勾选授权确认，上传小于 5MB 的图片。
6. 创建任务：打开 `/image-tools`，选择上传文件，创建 `image_compress` 任务。
7. 扣积分：任务成功后 `/credits` 出现 `consume` 流水。
8. 查看结果：打开 `/tasks` 或 `/files`。
9. 后台查看：用管理员 `LIU` 登录后打开 `/admin`，可看用户、订单、流水、文件、任务。

## 真实与 mock

真实实现：

- 用户注册登录
- token 鉴权
- 积分钱包
- 积分流水
- 订单创建
- mock 支付入账防重复
- 小图片/视频文件上传元数据
- 任务创建和扣积分事务
- Django Admin 数据管理
- 前端 SaaS 页面和 Anthropic 风格 UI

mock / 演示：

- 真实支付未接入
- 视频压缩、裁剪、转换、修复均为 mock
- 图片修复、封面裁剪、自有素材水印修复为 mock
- 图片压缩第一版生成演示结果，未引入 Pillow 做真实压缩
- 多平台发布只预留页面，不接平台

## 合规边界

只用于原创、已授权或拥有合法处理权的素材。不要用于平台去水印、搬运去水印、破解水印、无痕盗视频、全网视频去水印或绕过平台审核。

## 免费版限制

- Render Free 可能休眠，前端会显示服务唤醒/稍后重试提示
- 文件上传限制 5MB
- 文件先存本地/部署实例目录，TiDB 只存元数据
- 不适合长期保存生产文件
- 无真实支付
- 无真实视频处理

## 下一版

- 接入对象存储保存文件本体
- 接入真实支付 provider
- 接入 Pillow / FFmpeg Worker
- 加任务队列
- 加邮箱验证和密码找回
- 接入官方发布平台 API
- 增加审计日志和风控
