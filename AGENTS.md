# AGENTS.md - 个人网站项目约定

## 项目概述

个人网站项目，采用前后端分离架构：

- **后端**：Django 4.2 (Python 3.9) — API 服务 + 后台管理
- **前端**：Vue 3 + Vite 8 — 用户前台
- **数据库**：SQLite（开发环境）
- **后台主题**：SimpleUI

## 目录结构

```
个人网站/
├── manage.py                    # Django 管理入口
├── db.sqlite3                   # SQLite 数据库
├── personal_site/               # Django 项目配置
│   ├── settings.py              # 全局配置（CORS/SimpleUI/国际化）
│   ├── urls.py                  # 根路由（/admin/ + /api/）
│   ├── wsgi.py
│   └── asgi.py
├── website/                     # Django 主应用
│   ├── models.py                # 数据模型
│   ├── views.py                 # API 视图
│   ├── urls.py                  # 应用路由
│   ├── admin.py                 # 后台注册
│   └── migrations/              # 数据库迁移
├── frontend/                    # Vue 3 前端
│   ├── src/
│   │   ├── router/index.js      # 前端路由
│   │   ├── views/               # 页面组件（Home.vue, About.vue）
│   │   ├── layouts/             # 布局组件（MainLayout.vue）
│   │   ├── components/          # 公共组件
│   │   ├── api/index.js         # axios 封装（baseURL: /api）
│   │   ├── assets/              # 静态资源
│   │   ├── App.vue              # 根组件
│   │   └── main.js              # 入口
│   ├── vite.config.js           # Vite 配置（含 API 代理）
│   └── package.json
└── venv/                        # Python 虚拟环境
```

## 启动方式

### 同时启动前后端

```bash
# 终端 1：Django 后端（端口 8000）
cd /Volumes/D/个人网站 && source venv/bin/activate && python manage.py runserver

# 终端 2：Vue 前端（端口 5173）
cd /Volumes/D/个人网站/frontend && npx vite --host
```

### 访问地址

| 服务 | 地址 |
|------|------|
| Vue 前台 | http://127.0.0.1:5173 |
| Django Admin | http://127.0.0.1:8000/admin/ |
| Django API | http://127.0.0.1:8000/api/ |

### 管理员账号

- 用户名：LIU
- 密码：1234567890
- 邮箱：1276759989@qq.com
- 昵称：LEX

## 架构约定

### 前后端通信

- 前端通过 Vite proxy 将 `/api/*`、`/admin/*`、`/static/*` 代理到 Django（127.0.0.1:8000）
- API 请求统一走 `frontend/src/api/index.js`（axios 实例，baseURL: `/api`）
- CORS 已配置，允许 `localhost:5173` 和 `127.0.0.1:5173`

### 后端规范

- 所有 API 视图放在 `website/views.py`（或按模块拆分）
- 路由注册在 `website/urls.py`，主 urls.py 通过 `path('api/', include('website.urls'))` 挂载
- Model 变更后必须执行 `python manage.py makemigrations && python manage.py migrate`
- Admin 模型注册在 `website/admin.py`，SimpleUI 自动渲染后台

### 前端规范

- 页面放 `src/views/`，组件放 `src/components/`，布局放 `src/layouts/`
- 路由在 `src/router/index.js` 中配置，使用懒加载 `() => import(...)`
- 样式使用 `<style scoped>`，避免全局污染
- 组件命名：PascalCase（如 `UserProfile.vue`）

### 新增功能流程

1. 后端：在 `website/models.py` 定义模型 → `makemigrations` → `migrate`
2. 后端：在 `website/views.py` 写 API 视图 → `website/urls.py` 注册路由
3. 后端：如需后台管理，在 `website/admin.py` 注册模型
4. 前端：在 `src/views/` 创建页面 → `src/router/index.js` 添加路由
5. 前端：通过 `src/api/index.js` 调用后端 API

## 技术栈版本

| 技术 | 版本 |
|------|------|
| Python | 3.9.6 |
| Django | 4.2.30 |
| SimpleUI | latest |
| django-cors-headers | latest |
| Node.js | 22.x |
| Vue | 3.5.x |
| Vite | 8.x |
| vue-router | 4.x |
| axios | 1.x |

## 国际化

- Django 后台语言：`zh-hans`（简体中文）
- 时区：`Asia/Shanghai`

## 注意事项

- `venv/`、`node_modules/`、`db.sqlite3` 不要提交到 Git
- 修改 settings.py 后需重启 Django 服务
- 前端 build 产物可用于后续部署到 Nginx 或 CDN
