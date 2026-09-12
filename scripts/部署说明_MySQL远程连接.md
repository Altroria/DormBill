# MySQL 远程连接配置说明

## 一、Docker 端口映射配置

已在 `docker-compose.prod.yml` 中启用 MySQL 端口映射：
```yaml
ports:
  - "${DB_PORT:-3306}:3306"
```

## 二、服务器端配置步骤

### 1. 确保 .env 文件配置正确
在远程服务器上创建或编辑 `.env` 文件：
```bash
# 数据库配置
DB_PASSWORD=405649
DB_NAME=dormbill
DB_PORT=3306

# 后端配置
BACKEND_PORT=8000
DEBUG=False

# 前端配置
FRONTEND_PORT=80
VITE_API_URL=/api

# CORS 配置
CORS_ORIGINS=http://localhost,http://localhost:80
```

### 2. 启动或重启 Docker 容器
```bash
# 如果是首次部署
docker-compose -f docker-compose.prod.yml up -d

# 如果已经在运行，需要重启 MySQL 容器
docker-compose -f docker-compose.prod.yml restart mysql
```

### 3. 开放服务器防火墙端口

#### Ubuntu/Debian (ufw)
```bash
sudo ufw allow 3306/tcp
sudo ufw status
```

#### CentOS/RHEL (firewalld)
```bash
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

#### 阿里云/腾讯云安全组
在云服务器控制台的安全组规则中添加：
- 规则方向：入方向
- 授权策略：允许
- 协议类型：TCP
- 端口范围：3306
- 授权对象：
  - `0.0.0.0/0`（允许所有 IP，不推荐）
  - `你的本地IP/32`（推荐，仅允许你的 IP）

### 4. 验证端口是否开放
在本地电脑运行：
```bash
telnet 远程服务器IP 3306
```
或
```bash
nc -zv 远程服务器IP 3306
```

## 三、本地工具连接配置

### 1. 连接参数
- **主机/Host**: 远程服务器的公网IP地址
- **端口/Port**: 3306
- **用户名/Username**: root
- **密码/Password**: 405649
- **数据库/Database**: dormbill

### 2. 常用工具配置示例

#### Navicat
1. 新建连接 → MySQL
2. 连接名：DormBill 生产环境
3. 主机：远程服务器IP
4. 端口：3306
5. 用户名：root
6. 密码：405649
7. 测试连接 → 连接

#### MySQL Workbench
1. 点击 "+" 创建新连接
2. Connection Name: DormBill Production
3. Hostname: 远程服务器IP
4. Port: 3306
5. Username: root
6. Password: Store in Keychain → 输入 405649
7. Test Connection

#### DBeaver
1. 新建连接 → MySQL
2. Server Host: 远程服务器IP
3. Port: 3306
4. Database: dormbill
5. Username: root
6. Password: 405649
7. 测试连接

#### 命令行连接
```bash
mysql -h 远程服务器IP -P 3306 -u root -p
# 输入密码：405649
```

## 四、安全建议

### 1. 修改默认端口（可选）
在 `.env` 中修改：
```bash
DB_PORT=33060  # 改为非标准端口
```

### 2. 限制访问IP
修改 MySQL 配置或使用防火墙规则，仅允许特定IP访问。

### 3. 使用强密码
生产环境建议修改为更复杂的密码：
```bash
DB_PASSWORD=你的强密码
```

### 4. 创建专用远程用户（推荐）
进入 MySQL 容器创建只读用户：
```bash
# 进入容器
docker exec -it dormbill-mysql mysql -uroot -p405649

# 创建只读用户
CREATE USER 'readonly'@'%' IDENTIFIED BY '只读密码';
GRANT SELECT ON dormbill.* TO 'readonly'@'%';
FLUSH PRIVILEGES;
```

## 五、故障排查

### 问题1：连接超时
- 检查服务器防火墙是否开放 3306 端口
- 检查云服务器安全组规则
- 确认 Docker 容器正在运行：`docker ps | grep mysql`

### 问题2：连接被拒绝
- 检查 MySQL 容器是否正常：`docker logs dormbill-mysql`
- 确认端口映射：`docker port dormbill-mysql`

### 问题3：密码错误
- 检查 `.env` 文件中的 DB_PASSWORD
- 重置密码：
```bash
docker exec -it dormbill-mysql mysql -uroot -p
ALTER USER 'root'@'%' IDENTIFIED BY '新密码';
FLUSH PRIVILEGES;
```

### 问题4：无法访问特定数据库
```bash
# 检查数据库是否存在
docker exec -it dormbill-mysql mysql -uroot -p405649 -e "SHOW DATABASES;"
```

## 六、查看当前配置

```bash
# 查看容器端口映射
docker ps | grep mysql

# 查看 MySQL 容器日志
docker logs dormbill-mysql

# 查看监听端口
netstat -tuln | grep 3306
```
