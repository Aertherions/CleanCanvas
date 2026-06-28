# Clean Creation MVP — 部署指南

## 项目结构

```
个人网站/
├── personal_site/          # Django 项目配置
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── templates/admin/
├── website/                # Django app（模型、视图、管理后台）
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── migrations/
├── frontend/               # Vue 3 + Vite 前端
│   ├── src/
│   ├── public/
│   ├── vercel.json
│   └── vite.config.js
├── manage.py
├── requirements.txt
├── render.yaml
├── .env.example
└── README.md
```

---

## 一、本地开发

### 1. 后端

```bash
cd /Volumes/D/个人网站

# 创建虚拟环境（首次）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（首次 / 模型变更后）
python manage.py migrate

# 创建管理员（首次）
python manage.py createsuperuser

# 启动后端
python manage.py runserver 127.0.0.1:8000 --noreload
```

本地默认使用 SQLite（`db.sqlite3`），无需配置数据库环境变量。

### 2. 前端

```bash
cd /Volumes/D/个人网站/frontend

# 安装依赖（首次）
npm install

# 启动开发服务器
npm run dev -- --host 127.0.0.1
```

访问 http://127.0.0.1:5173/

前端通过 Vite proxy 将 `/api` 代理到 `http://127.0.0.1:8000`。

### 本地环境变量（可选）

如需自定义，可在项目根目录创建 `.env`：

```env
DEBUG=true
JWT_SECRET=your-dev-secret-key
```

---

## 二、后端部署（Render Free Web Service）

### 步骤

1. 将代码推送到 GitHub / GitLab 仓库
2. 登录 [Render Dashboard](https://dashboard.render.com/)
3. 点击 **New → Web Service**
4. 连接 Git 仓库，选择项目根目录
5. Render 会自动读取 `render.yaml`，或手动填写：
   - **Name**: `clean-creation-api`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn personal_site.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: Free
6. 配置环境变量（见下方）
7. 点击 **Create Web Service**

### Render 环境变量

| 变量名 | 值 | 说明 |
|---|---|---|
| `DEBUG` | `false` | 生产环境必须关闭 |
| `JWT_SECRET` | 随机字符串 | 用于 Django SECRET_KEY 和 Token 签名 |
| `ALLOWED_HOSTS` | `.onrender.com` | 允许 Render 域名 |
| `CORS_ALLOWED_ORIGINS` | `https://你的前端域名` | 前端正式域名 |
| `DATABASE_HOST` | TiDB Cloud 主机 | 生产数据库地址 |
| `DATABASE_PORT` | `4000` | TiDB 默认端口 |
| `DATABASE_USER` | TiDB 用户名 | |
| `DATABASE_PASSWORD` | TiDB 密码 | |
| `DATABASE_NAME` | `clean_creation_mvp` | 数据库名 |
| `DATABASE_SSL` | `true` | TiDB 需要 SSL |
| `DATABASE_SSL_CA` | CA 证书路径（可选） | TiDB Cloud 提供的 CA |
| `CREDIT_RATE` | `10` | 1 元 = 多少积分 |
| `MAX_UPLOAD_MB` | `5` | 上传文件大小限制 |
| `ENABLE_FFMPEG` | `false` | 视频处理开关 |

### Render Free 限制

- 实例空闲 15 分钟后自动休眠
- 首次请求需等待 30-60 秒唤醒
- 前端已内置唤醒提示（`ECONNABORTED` 时显示"服务正在唤醒"）
- 512 MB 内存
- 无持久化存储（上传文件重启后丢失）

---

## 三、前端部署（Vercel）

### 步骤

1. 登录 [Vercel](https://vercel.com/)
2. 点击 **New Project**
3. 导入 Git 仓库
4. 设置：
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Framework Preset**: Vite
5. 添加环境变量：
   - `VITE_API_BASE_URL` = `https://你的-render-api域名/api`
6. 点击 **Deploy**

`frontend/vercel.json` 已配置 SPA 路由回退。

---

## 四、前端部署（Cloudflare Pages 备选）

### 步骤

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 **Workers & Pages → Create → Pages**
3. 连接 Git 仓库
4. 设置：
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. 添加环境变量：
   - `VITE_API_BASE_URL` = `https://你的-render-api域名/api`
6. 部署

`frontend/public/_redirects` 已配置 SPA 路由回退（`/* /index.html 200`）。

---

## 五、数据库配置

### 本地开发（SQLite）

无需任何配置。当 `DATABASE_HOST` 环境变量不存在时，自动使用 SQLite。

### 生产环境（TiDB Cloud）

1. 登录 [TiDB Cloud](https://tidbcloud.com/)
2. 创建 Serverless Cluster：
   - Cloud Provider: Alibaba Cloud
   - Region: Singapore ap-southeast-1
   - Spending Limit: $0 / month
3. 在 **Connect** 页面获取连接信息
4. 在 Render 环境变量中填入 `DATABASE_HOST`、`DATABASE_PORT`、`DATABASE_USER`、`DATABASE_PASSWORD`、`DATABASE_NAME`
5. `DATABASE_SSL=true` 已默认开启

### 数据库 URL 格式（备选）

也支持通过 `DATABASE_URL` 配置：

```
mysql://USER:PASSWORD@HOST:4000/DATABASE?ssl={"ca":null}
```

当前 `settings.py` 使用 `DATABASE_HOST` 方式，按字段分开配置。

### 迁移

生产环境首次部署时，Render 的 Build Command 会自动执行 `python manage.py migrate`。

---

## 六、静态文件

- WhiteNoise 中间件已配置，自动在 production 环境 serve 静态文件
- `STATICFILES_STORAGE` 使用 `CompressedManifestStaticFilesStorage`
- Build Command 中 `collectstatic` 会在部署时收集所有静态资源

---

## 七、首次部署后

1. 访问后端 URL + `/admin/`，用超级管理员账号登录 Django Admin
2. 或通过前端 `/admin` 页面（API 管理后台）查看数据
3. 在前端注册新用户，测试完整流程
4. 如需手动添加积分，通过管理后台 `/api/admin/credits/adjust` 接口
