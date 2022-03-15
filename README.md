# fastapi 项目脚手架

###### 声明：此仓库仅做为 FastAPI 入门级参考，对于不同需求，使用者请自由扩展

📢 开箱即用，所有分支持续同步更新

😓 由于分支过多，不易维护， 所以你也可以在同类型分支之间 cv 功能从而自定义demo

## 异步：
### async -> [master](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/master/)
```text
fastapi + sqlalchyme + alembic + aiomysql + aioredis

📢: 含 redis 邮箱验证码登录
```

### async -> [async-CRUDBase](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/async-CRUDBase/)
```text
fastapi + sqlalchyme + alembic + aiomysql + aioredis

📢: 在 master 分支基础上扩展，对普通 CRUD 操作进行封装
```

### async -> [async+APScheduler](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/async%2BAPScheduler/)
```text
fastapi + sqlalchyme + alembic + aiomysql + aioredis + APScheduler

📢: 在 master 分支基础上扩展，加入 APScheduler 定时任务，新增了 redis 图片验证码登录
❌：去除了 redis 邮箱验证码登录方式
```

### async -> [async+Casbin-RBAC](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/async%2BCasbin-RBAC/)
```text
fastapi + sqlalchyme + alembic + aiomysql + aioredis + pycasbin

📢: 在 async-CRUDBase 分支基础上扩展，加入 pycasbin(RBAC) 授权
```

## 同步：
### sync -> [sync](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/sync/)
```text
fastapi + sqlalchyme + alembic + mysql + redis

📢: 含 redis 图片验证码登录
```

### sync -> [sync-CRUDBase](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/sync-CRUDBase/)
```text
fastapi + sqlalchyme + alembic + mysql + redis + APScheduler

📢: 在 sync 分支基础上扩展，对普通 CRUD 操作进行封装，加入 APScheduler 定时任务
```

### sync -> [sync-Plus](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/sync-Plus/)
```text
fastapi + sqlalchyme + alembic + mysql + redis + APScheduler + pycasbin

📢: 在 sync-CRUDBase 分支基础上扩展，加入 pycasbin(RBAC) 授权
```

## 下载：
```shell
windows:
git clone https://gitee.com/wu_cl/fastapi_mysql_demo.git

linux:
wget https://gitee.com/wu_cl/fastapi_mysql_demo/repository/archive/master.zip
```

## 安装使用:
### 1：传统：
first > 项目根目录下安装所需依赖包
```shell
pip install -r requirements.txt
```

next > 配置数据库，执行迁移
```text
1 > 修改 core/conf.py 文件中数据库配置: # DB

2 > 终端进入 backend/app/ 目录下, 生成迁移文件
    执行: alembic revision --autogenerate

3 > 执行迁移: alembic upgrade head

4 > 运行 init_test_data.py 文件，初始化用户数据
```

end > 运行 main.py 文件启动 FastAPI

### 2：docker
###### 😓待完善

## 结构树
结构树基本大致相同，详情请查看源代码

```text
├── backend
│   └── app
│       ├── alembic
│       │   ├── env.py
│       │   ├── README
│       │   └── script.py.mako
│       ├── alembic.ini
│       ├── api
│       │   ├── __init__.py
│       │   ├── jwt_security.py
│       │   └── v1
│       │       ├── __init__.py
│       │       ├── test_redis.py
│       │       └── user.py
│       ├── common
│       │   ├── __init__.py
│       │   ├── log.py
│       │   ├── pagination.py
│       │   └── sys_redis.py
│       ├── core
│       │   ├── conf.py
│       │   ├── __init__.py
│       │   └── path_conf.py
│       ├── crud
│       │   ├── __init__.py
│       │   └── user_crud.py
│       ├── datebase
│       │   ├── base_class.py
│       │   ├── db_mysql.py
│       │   └── __init__.py
│       ├── middleware
│       │   ├── access_middle.py
│       │   └── __init__.py
│       ├── model
│       │   ├── __init__.py
│       │   └── user.py
│       ├── schemas
│       │   ├── __init__.py
│       │   ├── sm_token.py
│       │   └── sm_user.py
│       ├── test
│       │   └── __init__.py
│       |── utils
│       |   ├── generate_uuid.py
│       |   ├── __init__.py
│       |   ├── pydantic_as_form.py
│       |   └── send_email_verification_code.py
│       ├── __init__.py
│       ├── init_test_data.py
│       └─ main.py
├── LICENSE
├── README.md
└── requirements.txt
```