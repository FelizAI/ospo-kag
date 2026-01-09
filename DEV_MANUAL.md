# 开发环境搭建

## 1 项目结构

```
  .          
  ├── LICENSE                         # License 申明        
  ├── README.md           
  ├── apps                            # 后端项目根目录        
  │ ├── application                   # 应用管理
  │ ├── chat                          # 对话相关
  │ ├── common                        # 公共模块
  │ ├── knowledge                     # 知识库管理
  │ ├── local_model                   # 本地模型服务
  │ ├── maxkb                         # Django 项目配置
  │ ├── models_provider               # 模型供应商
  │ ├── system_manage                 # 系统管理
  │ ├── tools                         # 工具/插件
  │ ├── users                         # 用户管理          
  │ └── manage.py                     # Django 管理命令入口         
  ├── installer                       # 安装相关  
  ├── docker-compose.yml              # 应用 Docker编排
  ├── docker-compose-middleware.yml   # 中间件 Docker编排 (PG, Redis)
  ├── pyproject.toml                  # 后端依赖配置         
  └── ui                              # 前端项目根目录          
    ├── package.json                  # 前端依赖配置             
    ├── vite.config.ts                # Vite 配置              
    └── src                           # 前端源码
```     

## 2 环境准备          

  - **前端环境准备**       
    安装 [Node.js](https://nodejs.org/) ，推荐 v24 版本。     
  - **后端环境准备**        
    需要 Linux 环境 (推荐 Ubuntu/CentOS) 或 macOS。
    安装 [Python](https://www.python.org/downloads/) ，版本 v3.11.x。
    安装 [Poetry](https://python-poetry.org/docs/) 包管理器。
  - **中间件环境**   
    安装 [Docker](https://www.docker.com/) 和 Docker Compose。
    项目依赖 PostgreSQL (v17, pgvector) 和 Redis (v7)，推荐使用 Docker 启动。

## 3 本地配置

### 3.1 启动中间件

 
  使用 Docker Compose 启动 PostgreSQL 和 Redis 服务。

  ``` bash
  # 启动中间件
  docker-compose -f docker-compose-middleware.yml up -d
  ```
  
  默认端口映射：
  - PostgreSQL: 35432 (容器内 5432)
  - Redis: 36379 (容器内 6379)

### 3.2 后端配置

 
  在项目根目录下创建 `.env` 文件，配置数据库和 Redis 连接信息（覆盖默认配置）。
  
  ```bash
  # .env 文件示例
  
  # 数据库配置 (对应 docker-compose-middleware.yml 的端口)
  MAXKB_DB_HOST=127.0.0.1
  MAXKB_DB_PORT=35432
  MAXKB_DB_USER=root
  MAXKB_DB_PASSWORD=Password
  MAXKB_DB_NAME=maxkb
  
  # Redis 配置
  MAXKB_REDIS_HOST=127.0.0.1
  MAXKB_REDIS_PORT=36379
  MAXKB_REDIS_PASSWORD=Password
  ```

### 3.3 初始化数据库

  配置完成后，需要初始化数据库结构。

  ```bash
  # 安装后端依赖
  poetry install
  
  # 初始化/升级数据库
  python main.py upgrade_db
  ```

## 4 开发调试

### 4.1 启动后端


  后端服务包含 Web 服务、Celery 任务队列和本地模型服务。
  
  ```bash
  # 启动所有服务 (Web + Celery + Local Model)
  python main.py start
  ```
  
  或者分别启动各个服务（用于调试）：
  
  ```bash
  # 启动 Web 服务 (默认端口 8080)
  python main.py dev web
  
  # 启动 Celery Worker
  python main.py dev celery
  
  # 启动本地模型服务
  python main.py dev local_model
  ```



### 4.2 启动前端



  ```bash
  cd ui
  
  # 安装依赖
  npm install
  
  # 启动开发服务器
  npm run dev
  ```

  启动成功后，浏览器访问控制台显示的地址 (通常是 http://localhost:5173)。
  前端会代理 `/admin/api`, `/chat/api` 等请求到后端的 8080 端口。


## 5 访问项目


  前后端都启动成功后，通过浏览器访问前端地址。
  
  默认管理员账号：`admin`
  默认密码：`MaxKB@123..` (具体请参照安装文档或初始设定)


