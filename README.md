# 蓉蓉的收租小工具 - 宿舍房租水电费用管理系统

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Vue3](https://img.shields.io/badge/Vue-3.4+-brightgreen.svg)](https://vuejs.org/)
[![Element Plus](https://img.shields.io/badge/Element%20Plus-2.6+-409EFF.svg)](https://element-plus.org/)

> 基于 PRD V1.1 的宿舍费用月度/双月结算系统

## 📋 项目概述

**系统定位**：行政内部宿舍费用月度/双月结算系统  
**核心目标**：每月/每两个月快速、准确计算员工宿舍费用，生成最终扣款表

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端 | Python 3.10 + FastAPI | 高性能异步API框架 |
| ORM | SQLAlchemy 2.0 + Pydantic v2 | 类型安全、数据验证 |
| 数据库 | MySQL 8.0 | 关系型数据库 |
| 前端 | Vue 3 + TypeScript + Vite | 响应式、类型安全 |
| UI | Element Plus | Vue3 生态成熟组件库 |
| Excel | openpyxl (后端) + xlsx (前端) | 导入导出 |

### 核心功能

✅ **基础资料管理**：楼栋、房间、员工、入住记录  
✅ **月度电费管理**：普通电表 + 空调电表抄表、自动计算、平均分摊、尾差处理  
✅ **双月水费管理**：水费账单录入、半月规则分摊  
✅ **月度结算**：自动生成员工扣款、支持手动调整、锁定机制  
✅ **Excel 导入导出**：员工批量导入、扣款表/电费明细/水费明细导出  
✅ **特殊规则**：试用期免租、夫妻间费用、出差豁免、换房折算

## 🚀 快速开始

### 部署方式

本项目支持两种部署方式：

1. **🐳 Docker 部署（推荐）**：一键部署，无需安装依赖
2. **📦 传统部署**：手动安装 Python、Node.js、MySQL

---

### 方式一：Docker 部署（推荐）⭐

#### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

#### 快速部署

**Windows (PowerShell):**

```powershell
# 1. 复制环境配置
Copy-Item .env.docker .env

# 2. 修改 .env 中的数据库密码（重要！）
notepad .env

# 3. 一键部署
docker-compose up -d

# 4. 查看服务状态
docker-compose ps

# 5. 访问系统
# 前端: http://localhost
# 后端文档: http://localhost:8000/docs
```

**Linux/macOS:**

```bash
# 1. 复制环境配置
cp .env.docker .env

# 2. 修改 .env 中的数据库密码（重要！）
vim .env

# 3. 一键部署
docker-compose up -d

# 4. 查看服务状态
docker-compose ps

# 5. 访问系统
# 前端: http://localhost
# 后端文档: http://localhost:8000/docs
```

**使用部署脚本（更简单）:**

```bash
# Windows
.\scripts\deploy.ps1 dev

# Linux/macOS
chmod +x scripts/deploy.sh
./scripts/deploy.sh dev
```

#### Docker 常用命令

```bash
# 查看日志
docker-compose logs -f

# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 停止并删除容器（保留数据）
docker-compose down

# 备份数据库
docker-compose exec mysql mysqldump -uroot -p dormbill > backup.sql
```

📖 **完整的 Docker 部署文档**: [DOCKER_DEPLOY.md](./DOCKER_DEPLOY.md)

---

### 方式二：传统部署

#### 前置要求

- Python 3.10+
- Node.js 16+
- MySQL 8.0+

#### 1. 克隆项目

```bash
cd E:\cursor\DormBill
```

### 2. 后端配置

#### 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 配置数据库

1. 创建数据库：
```sql
CREATE DATABASE dormbill CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 编辑 `backend/.env`（已从 .env.example 复制）：
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的密码
DB_NAME=dormbill
```

#### 启动后端

```bash
python run.py
```

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 3. 前端配置

#### 安装依赖

```bash
cd frontend
npm install
```

#### 配置 API 地址

编辑 `frontend/.env`：
```env
VITE_API_URL=http://localhost:8000/api
```

#### 启动前端

```bash
npm run dev
```

访问：http://localhost:5173

---

## 🐳 Docker 架构

### 容器组成

```
┌─────────────────────────────────────────┐
│         前端容器 (Nginx)                 │
│     http://localhost:80                 │
│  - 提供静态文件服务                       │
│  - 反向代理 /api 到后端                  │
└──────────────┬──────────────────────────┘
               │
               ├─► /api/* ────────────────┐
               │                          │
┌──────────────▼──────────────────────────▼──┐
│         后端容器 (FastAPI)                  │
│     http://backend:8000                    │
│  - RESTful API 服务                        │
│  - 业务逻辑处理                             │
└──────────────┬────────────────────────────┘
               │
               │ MySQL 连接
               │
┌──────────────▼────────────────────────────┐
│         数据库容器 (MySQL 8.0)             │
│     mysql:3306                            │
│  - 持久化数据存储                          │
│  - 数据卷: mysql_data                     │
└───────────────────────────────────────────┘
```

### 镜像信息

| 容器 | 基础镜像 | 大小（约） | 端口 |
|------|----------|-----------|------|
| frontend | nginx:1.25-alpine | 50 MB | 80 |
| backend | python:3.10-slim | 350 MB | 8000 |
| mysql | mysql:8.0 | 600 MB | 3306 |

### 数据持久化

- **mysql_data**: MySQL 数据目录（/var/lib/mysql）
- 即使删除容器，数据仍然保留
- 使用 `docker-compose down -v` 才会删除数据卷

### 网络配置

- 容器间通过 `dormbill-network` 桥接网络通信
- 前端通过服务名 `backend` 访问后端
- 后端通过服务名 `mysql` 访问数据库

---

## 📁 项目结构

```
DormBill/
├── backend/                # 后端 FastAPI
│   ├── app/
│   │   ├── main.py        # 应用入口
│   │   ├── config.py      # 配置
│   │   ├── database.py    # 数据库连接
│   │   ├── models/        # ORM 模型（8个表）
│   │   ├── schemas/       # Pydantic 请求/响应模型
│   │   ├── routers/       # API 路由（10个模块）
│   │   ├── services/      # 业务逻辑（6个核心服务）
│   │   └── utils/         # 工具函数（日期/金额计算）
│   ├── requirements.txt
│   ├── Dockerfile         # 🐳 后端 Docker 镜像
│   ├── .dockerignore
│   └── run.py
├── frontend/              # 前端 Vue3
│   ├── src/
│   │   ├── api/          # API 客户端（8个模块）
│   │   ├── components/   # 公共组件
│   │   ├── views/        # 页面（7个主要页面）
│   │   ├── router/       # 路由配置
│   │   ├── styles/       # 全局样式
│   │   └── types/        # TypeScript 类型定义
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile         # 🐳 前端 Docker 镜像
│   ├── nginx.conf         # 🐳 Nginx 配置
│   ├── .dockerignore
│   └── .env.production    # 生产环境配置
├── docs/                  # 文档
│   └── init_database.sql
├── scripts/               # 部署脚本
│   ├── deploy.sh          # Linux/macOS 部署脚本
│   └── deploy.ps1         # Windows 部署脚本
├── tests/                 # 后端测试
│   └── test_core.py      # 核心计算测试（29个测试用例）
├── docker-compose.yml     # 🐳 Docker 编排（开发）
├── docker-compose.prod.yml # 🐳 Docker 编排（生产）
├── .env.docker            # 环境变量模板
├── .dockerignore
├── DOCKER_DEPLOY.md       # 🐳 Docker 部署完整文档
└── README.md
```

## 🧪 测试

### 后端单元测试

```bash
cd E:\cursor\DormBill
python -m pytest tests/test_core.py -v
```

**测试覆盖**：
- ✅ 金额计算与尾差处理（7个测试）
- ✅ 日期计算与入住天数（11个测试）
- ✅ 房租折算与试用期免租（5个测试）
- ✅ 电费分摊（3个测试）
- ✅ 水费分摊（2个测试）
- ✅ 最终扣款公式（1个测试）

**所有 29 个测试用例均通过 ✓**

### 前端开发测试

```bash
cd frontend
npm run build  # 生产构建测试
```

## 📊 核心业务规则

### 电费计算（每月）

```
房间电费 = 用电量 × 电价
个人普通电费 = 房间电费 ÷ 有效入住人数（含尾差处理）

房间空调电费 = 空调度数 × 空调平均单价
个人空调电费 = 房间空调电费 ÷ 有效入住人数（含尾差处理）
```

### 房租计算（按天折算）

```
实扣房租 = 房租标准 × 入住天数 ÷ 当月总天数
试用期内：实扣房租 = 0
```

### 水费分摊（双月）

```
半月规则：该月有效天数 > 15天 → 参与分摊
楼栋有效总人数 = Σ（每间房的有效入住人数）
每人水费 = 楼栋水费 ÷ 楼栋有效总人数（含尾差处理）
```

### 最终扣款

```
最终扣款 = 实扣房租 + 个人普通电费 + 个人空调电费 + 个人水费 - 补扣- + 补扣+
```

### 特殊规则

- **试用期免租**：试用期月数内，实扣房租 = 0
- **夫妻间**：主要缴费人承担全部水电费，另一人水电费 = 0
- **出差**：当月不计水电费，房租正常
- **换房**：按实际天数折算旧房和新房的房租

## 🎨 界面预览

### 配色方案（温馨风格）

- 主色调：`#6366F1` (靛蓝紫 - 专业温暖)
- 辅助色：`#F59E0B` (琥珀橙 - 收租/金额强调)
- 成功色：`#10B981` (翠绿)
- 背景色：`#F8FAFC` (浅灰白)
- 文字主色：`#1E293B`
- 文字辅色：`#64748B`

### 核心页面

1. **首页仪表盘**：统计卡片、金额汇总、试用期到期提醒
2. **楼栋管理**：CRUD 操作
3. **房间管理**：批量新增、楼栋筛选
4. **入住管理**：批量搬离/换房、状态色彩标识、试用期提醒
5. **员工管理**：Excel 导入、分页表格
6. **电表管理**：月度初始化、批量计算、导出明细
7. **水费管理**：账单录入、分摊明细可编辑
8. **结算管理**：预检查、生成结算、锁定/解锁、汇总统计

## 📦 部署

### Docker 部署（推荐）

**开发环境：**

```bash
# Windows
.\scripts\deploy.ps1 dev

# Linux/macOS
./scripts/deploy.sh dev
```

**生产环境：**

```bash
# 1. 修改 .env 中的密码和配置
vim .env

# 2. 部署
# Windows
.\scripts\deploy.ps1 prod

# Linux/macOS
./scripts/deploy.sh prod
```

详细文档：[DOCKER_DEPLOY.md](./DOCKER_DEPLOY.md)

---

### 传统部署（不使用 Docker）

#### 生产环境后端

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 生产环境前端

```bash
cd frontend
npm run build
# 将 dist/ 目录部署到 Nginx
```

#### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔧 开发指南

### 后端开发

- 所有金额计算使用 `Decimal`，禁止 `float`
- 金额保留两位小数，四舍五入 `ROUND_HALF_UP`
- 日期计算使用 `date_utils.py` 工具函数
- 尾差处理使用 `allocate_with_remainder()`
- 核心业务逻辑放在 `services/` 层

### 前端开发

- 金额显示格式：`¥{value.toFixed(2)}`
- 日期选择器：`format="YYYY-MM-DD"` `value-format="YYYY-MM-DD"`
- 月份选择器：`format="YYYY-MM"` `value-format="YYYY-MM-DD"`
- 删除操作前用 `ElMessageBox.confirm` 确认
- 使用 TypeScript 严格模式

### API 路由

| 模块 | 端点 | 说明 |
|------|------|------|
| 楼栋 | `/api/buildings` | CRUD |
| 房间 | `/api/rooms` | CRUD + 批量新增 |
| 员工 | `/api/employees` | CRUD + 导入 |
| 入住 | `/api/residences` | CRUD + 批量搬离/换房 |
| 电表 | `/api/meters` | 查询/更新/初始化/计算 |
| 水费 | `/api/water-expenses` | CRUD + 生成分摊 |
| 结算 | `/api/settlements` | 预检查/生成/锁定/解锁 |
| 仪表盘 | `/api/dashboard` | 统计数据 |
| 导出 | `/api/export/*` | Excel 导出 |
| 导入 | `/api/import/*` | Excel 导入 |

## 🐛 故障排查

### 后端启动失败

1. **数据库连接失败**：检查 MySQL 服务是否启动，`.env` 配置是否正确
2. **端口占用**：修改 `.env` 中的 `SERVER_PORT`
3. **模块导入错误**：确保已安装 `requirements.txt` 中的所有依赖

### 前端启动失败

1. **依赖安装失败**：删除 `node_modules` 和 `package-lock.json`，重新 `npm install`
2. **API 连接失败**：检查后端是否启动，`.env` 中的 `VITE_API_URL` 是否正确
3. **端口占用**：修改 `vite.config.ts` 中的 `server.port`

### 常见业务问题

1. **电表异常（本月读数 < 上月读数）**：系统会标记为 `abnormal`，需手动处理
2. **水费分摊不均**：检查半月规则是否生效，确认入住天数计算正确
3. **结算金额不对**：检查电费、水费是否已录入，试用期、出差等特殊状态是否正确

## 📝 版本历史

### v1.1.0 (2026-09-10)

🐳 Docker 部署支持
- 完整的 Docker 容器化方案
- docker-compose.yml（开发环境）
- docker-compose.prod.yml（生产环境）
- 一键部署脚本（Windows/Linux/macOS）
- 完整的 Docker 部署文档
- Nginx 反向代理配置
- 健康检查和自动重启
- 数据持久化和备份方案

### v1.0.0 (2026-09-09)

✅ 初始版本发布
- 后端 FastAPI + SQLAlchemy 完整实现
- 前端 Vue3 + Element Plus 全部页面
- 29 个单元测试全部通过
- 完整的 CRUD、批量操作、导入导出
- 核心计算逻辑（电费/房租/水费/结算）
- 特殊规则支持（试用期/夫妻间/出差/换房）

## 🤝 贡献

本项目为内部使用系统，如有问题或建议，请联系项目负责人。

## 📄 许可证

内部项目，保留所有权利。

---

**蓉蓉的收租小工具** - 让宿舍费用管理更简单 💰
