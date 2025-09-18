# 代码生成时间: 2025-09-18 21:06:13
import asyncio
from aiomysql import create_pool
from sanic import Sanic, response
from sanic.exceptions import ServerError, SanicException
from sanic.request import Request

# 数据库配置信息
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "your_username",
    "password": "your_password",
    "db": "your_database"
}

# 初始化Sanic应用
app = Sanic("DatabasePoolManagement")

# 创建数据库连接池
async def create_db_pool():
    return await create_pool(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        db=DB_CONFIG["db"],
        loop=app.loop
    )

# 定义关闭数据库连接池的方法
@app.listener("before_server_stop")
async def close_db_pool(app, loop):
    db_pool = app.ctx.db_pool
    if db_pool:
        await db_pool.close()
        await db_pool.wait_closed()

# 获取数据库连接池
@app.middleware("request")
async def add_db_pool_middleware(request: Request):
    request.ctx.db_pool = app.ctx.db_pool

# 定义一个测试路由，用于验证数据库连接池
@app.route("/test", methods=["GET"])
async def test(request: Request):
    db_pool = request.ctx.db_pool
    if not db_pool:
        raise ServerError("Database pool is not initialized.")
    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT VERSION()")
                version = await cur.fetchone()
                return response.json({"message": "Database connection successful", "version": version[0]})
    except Exception as e:
        raise SanicException(f"Database error: {e}", status_code=500)

if __name__ == "__main__":
    # 创建数据库连接池
    app.ctx.db_pool = asyncio.run(create_db_pool())
    # 启动Sanic应用
    app.run(host="0.0.0.0", port=8000)