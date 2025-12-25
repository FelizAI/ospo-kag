# MaxKB 中间件 Docker Compose

使用 Docker Compose 启动 MaxKB 所需的 PostgreSQL 和 Redis 中间件。

## 快速开始

```bash
# 启动服务
docker-compose -f docker-compose-middleware.yml up -d

# 查看状态（等待显示 healthy）
docker-compose -f docker-compose-middleware.yml ps

# 停止服务
docker-compose -f docker-compose-middleware.yml down
```

## 服务说明

### PostgreSQL 17 with pgvector
- **端口**: 5432
- **数据库**: maxkb
- **用户**: root / Password123@postgres
- **特性**: 自动创建数据库并安装 pgvector 扩展

### Redis 7
- **端口**: 6379
- **密码**: Password123@redis
- **特性**: AOF+RDB 持久化，1GB 内存限制

## 验证服务

```bash
# 验证 PostgreSQL（包括 pgvector 扩展）
docker exec maxkb-postgres pg_isready -U root -d maxkb
docker exec maxkb-postgres psql -U root -d maxkb -c "\dx" | grep vector

# 验证 Redis
docker exec maxkb-redis redis-cli -a Password123@redis ping
```

## 数据持久化

- PostgreSQL: `./data/postgres_data/`
- Redis: `./data/redis_data/`

## 注意事项

1. **首次启动**: 需要 30-60 秒初始化，等待健康检查显示 `healthy`
2. **生产环境**: 请修改 `docker-compose-middleware.yml` 和 `config.yml` 中的默认密码
3. **依赖准备**: 所有依赖（pgvector 扩展、数据库创建）都会自动完成，无需额外操作

## 连接信息

MaxKB 应用使用以下配置连接（与 `config.yml` 对应）：

```yaml
# PostgreSQL
DB_HOST: 127.0.0.1
DB_PORT: 5432
DB_USER: root
DB_PASSWORD: Password123@postgres
DB_NAME: maxkb

# Redis
REDIS_HOST: 127.0.0.1
REDIS_PORT: 6379
REDIS_PASSWORD: Password123@redis
REDIS_DB: 0
```
