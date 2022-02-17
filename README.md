# fastapi 项目脚手架

### async -> [master](https://gitee.com/wu_cl/fastapi_mysql_demo/tree/master/)
fastapi + sqlalchyme + alembic + aiomysql + aioredis

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