# fastapi 项目脚手架

### async -> [master](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/master/)
fastapi + sqlalchyme + alembic + aiomysql + aioredis

PS: 含 redis 邮箱登录

### async -> [APScheduler](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/async%2BAPScheduler/)
fastapi + sqlalchyme + alembic + aiomysql + aioredis + APScheduler

PS: 含 redis 图片验证码登录

### sync -> [sync](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/sync/)
fastapi + sqlalchyme + alembic + mysql + aioredis

## 迁移:
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

## 结构树

结构树基本大致相同，详情查看源代码

```text
D:.
├─.idea
│  └─inspectionProfiles
└─backend
    └─app
        ├─alembic
        ├─api
        │  ├─v1
        │  │  └─__pycache__
        │  └─__pycache__
        ├─common
        │  └─__pycache__
        ├─core
        │  └─__pycache__
        ├─crud
        │  └─__pycache__
        ├─datebase
        │  └─__pycache__
        ├─log
        ├─middleware
        │  └─__pycache__
        ├─model
        │  └─__pycache__
        ├─schemas
        │  └─__pycache__
        ├─static
        │  └─media
        │      └─uploads
        ├─test
        ├─utils
        │  └─__pycache__
        └─__pycache__

```