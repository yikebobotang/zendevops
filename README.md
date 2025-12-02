# 部署平台

一个基于Vue 3和Python Flask的现代化部署平台，支持多种中间件服务的配置和部署。

## 项目简介

本项目是一个功能完备的部署平台，通过Web页面可以轻松部署MySQL、Redis、ZooKeeper等中间件服务。平台采用前后端分离架构，后端集成Ansible进行实际部署操作，提供了完整的用户管理、部署配置和日志查看功能。

## 技术栈

### 前端
- Vue 3 + Vite
- Element Plus
- Vue Router
- Axios

### 后端
- Python Flask
- Flask-JWT-Extended
- Flask-CORS
- Ansible Runner
- PyJWT
- Bcrypt

## 项目结构

```
deploy-platform/
├── frontend/          # 前端代码
│   ├── src/           # 源代码
│   │   ├── components/ # 组件
│   │   ├── views/      # 页面
│   │   ├── router/     # 路由
│   │   └── main.js     # 入口文件
│   ├── index.html      # HTML模板
│   ├── vite.config.js  # Vite配置
│   └── package.json    # 依赖配置
├── backend/           # 后端代码
│   ├── app/            # 应用代码
│   │   ├── routes/     # 路由
│   │   └── __init__.py # 应用初始化
│   ├── config.py       # 配置文件
│   ├── app.py          # 入口文件
│   └── requirements.txt # 依赖配置
└── README.md           # 项目说明
```

## 功能特性

### 1. 用户管理
- 用户登录/退出
- 用户列表展示
- 添加新用户
- 编辑用户信息
- 删除用户
- 角色管理（管理员/普通用户）

### 2. 部署配置
- 服务类型选择（MySQL、Redis、ZooKeeper等）
- 动态配置参数表单
- 配置参数默认值
- 部署任务提交

### 3. 部署日志
- 部署历史记录
- 日志列表展示
- 日志详情查看
- 日志搜索功能

## 快速开始

### 环境要求
- Node.js >= 16.x
- Python >= 3.8
- Ansible >= 2.10

### 安装步骤

#### 1. 克隆项目
```bash
git clone <repository-url>
cd zendevops
```

#### 2. 前端安装
```bash
cd deploy-platform/frontend
npm install
```

#### 3. 后端安装
```bash
cd ../backend
pip install -r requirements.txt
```

### 运行项目

#### 1. 启动后端服务
```bash
python app.py
# 服务将运行在 http://localhost:5000
```

#### 2. 启动前端服务
```bash
cd ../frontend
npm run dev
# 服务将运行在 http://localhost:3000
```

### 访问项目

打开浏览器访问 `http://localhost:3000`，使用以下默认账号登录：
- 用户名：admin
- 密码：admin123

## API接口

### 用户认证
- `POST /api/login` - 用户登录

### 用户管理
- `GET /api/users` - 获取用户列表
- `POST /api/users` - 创建用户
- `PUT /api/users/:id` - 更新用户
- `DELETE /api/users/:id` - 删除用户

### 部署管理
- `GET /api/services` - 获取服务列表
- `POST /api/deploy` - 提交部署任务

### 日志管理
- `GET /api/logs` - 获取日志列表
- `GET /api/logs?deploy_id=xxx` - 获取指定部署日志

## 部署说明

### 生产环境部署

#### 1. 构建前端
```bash
cd deploy-platform/frontend
npm run build
# 构建产物将生成在 dist 目录
```

#### 2. 部署后端
- 使用 Gunicorn 或 uWSGI 部署 Flask 应用
- 配置 Nginx 反向代理
- 配置 SSL 证书

### Ansible 配置

- 确保 Ansible 已正确安装
- 配置 Ansible 主机清单
- 确保部署用户有足够的权限

## 开发说明

### 前端开发

```bash
cd deploy-platform/frontend
npm run dev
```

### 后端开发

```bash
cd deploy-platform/backend
python app.py
```

### 代码规范
- 前端使用 ESLint 进行代码检查
- 后端使用 PEP 8 代码规范

## 注意事项

1. 首次运行时，确保后端服务先启动
2. 部署服务时，确保目标主机已添加到 Ansible 主机清单
3. 生产环境中，建议修改默认的 JWT 密钥
4. 定期清理日志文件，避免占用过多磁盘空间

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请联系项目维护者。

---

© 2025 部署平台