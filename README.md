# fastapi 项目脚手架

开箱即用，所有分支持续同步更新

### async -> [master](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/master/)
fastapi + sqlalchyme + alembic + aiomysql + aioredis

PS: 含 redis 邮箱验证码登录

### async -> [APScheduler](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/async%2BAPScheduler/)
fastapi + sqlalchyme + alembic + aiomysql + aioredis + APScheduler

PS: 含 redis 图片验证码登录

### async -> [Casbin-RBAC](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/async%2BCasbin-RBAC/)
fastapi + sqlalchyme + alembic + aiomysql + aioredis + PyCasbin

###### rbac仅为简单嵌入，实际使用待后续完善

PS: 含 redis 邮箱验证码登录

### sync -> [sync](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/sync/)
fastapi + sqlalchyme + alembic + mysql + redis + PyCasbin(同上) + APScheduler

PS: 含 redis 图片验证码登录

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
###### 待完善

## 结构树
结构树基本大致相同，详情查看源代码

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