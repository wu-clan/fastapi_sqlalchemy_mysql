# FastAPI Project Demo

###### 声明：此仓库仅做为 FastAPI 入门级参考

📢 开箱即用, 所有接口采用 restful 风格

## 分支说明

### 异步：

#### async -> master

```text
fastapi + sqlalchyme + alembic + aiomysql + aioredis

📢: 含 redis 邮箱验证码登录
```

#### async -> async-APScheduler

```text
fastapi + sqlalchyme + alembic + aiomysql + aioredis + APScheduler

📢: 在 master 分支基础上扩展, 加入 APScheduler 定时任务
✨: 删除了邮箱验证码登录, 新增了图片验证码登录
❗：很遗憾，此分支已停止维护，仅作为异步图形验证码登陆保留
```

#### async -> async-CRUDBase

```text
fastapi + sqlalchyme + alembic + aiomysql + aioredis + APScheduler

📢: 在 master 分支基础上扩展，对普通 CRUD 操作进行封装，加入 APScheduler 定时任务
```

#### async -> async-Plus

```text
fastapi + sqlalchyme + alembic + aiomysql + aioredis + APScheduler + pycasbin

📢: 在 async-CRUDBase 分支基础上扩展，加入 RBAC 鉴权
```

### 同步：

#### sync -> sync

```text
fastapi + sqlalchyme + alembic + pymysql + redis

📢: 含 redis 图片验证码登录
```

#### sync -> sync-CRUDBase

```text
fastapi + sqlalchyme + alembic + pymysql + redis + APScheduler

📢: 在 sync 分支基础上扩展，对普通 CRUD 操作进行封装，加入 APScheduler 定时任务
```

#### sync -> sync-Plus

```text
fastapi + sqlalchyme + alembic + pymysql + redis + APScheduler + pycasbin

📢: 在 sync-CRUDBase 分支基础上扩展，加入 RBAC 鉴权
```

## 下载：

### 1. 克隆仓库

```shell
# 全部分支:
git clone https://gitee.com/wu_cl/fastapi_sqlalchemy_mysql.git

# 指定分支:
git clone -b 分支名 https://gitee.com/wu_cl/fastapi_sqlalchemy_mysql.git
```

### 2. 使用 CLI

[跳转 Gitee](https://gitee.com/wu_cl/fastapi_ccli)

[跳转 GitHub](https://github.com/wu-clan/fastapi_ccli)

## 安装使用:

> ⚠️: 此过程请格外注意端口占用情况, 特别是 8000, 3306, 6379...

### 1：传统

1. 安装依赖
    ```shell
    pip install -r requirements.txt
    ```

2. 创建数据库 fsmp, 选择 utf8mb4 编码
3. 查看 backend/app/core/conf.py 配置文件, 检查并修改数据库配置信息
4. 执行数据库迁移 [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
    ```shell
    cd backend/app/
    
    # 生成迁移文件
    alembic revision --autogenerate
    
    # 执行迁移
    alembic upgrade head
    ```

5. 安装启动 redis
6. 查看 backend/app/core/conf.py 配置文件, 检查并修改 redis 配置信息
7. 执行 backend/app/main.py 文件启动服务
8. 浏览器访问: http://127.0.0.1:8000/v1/docs

---

### 2：docker

1. 在 docker-compose.yml 文件所在目录下执行一键启动命令

    ```shell
    docker-compose up -d --build
    ```
2. 等待命令自动执行完成

3. 浏览器访问: http://127.0.0.1:8000/v1/docs

## 初始化测试数据

执行 backend/app/init_test_data.py 文件

## 目录结构

结构树基本大致相同，详情请查看源代码

```text
├── backend
│   └── app
│       ├── alembic
│       ├── api
│       │   └── v1
│       ├── common
│       ├── core
│       ├── crud
│       ├── database
│       ├── middleware
│       ├── models
│       ├── schemas
|       |—— static
│       ├── test
│       └── utils
├── LICENSE
├── README.md
└── requirements.txt
```