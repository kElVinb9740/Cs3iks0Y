# 代码生成时间: 2025-08-22 06:01:31
import sanic
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.response import json
from peewee import *

# 数据库配置
db = PostgresqlDatabase('my_database', user='sanic_user', password='sanic_password', host='localhost')

# 定义数据模型
class BaseModel(Model):
    """peewee.Model的基类，用于管理数据库连接和初始化"""
    class Meta:
        database = db

class User(BaseModel):
    """用户模型"""
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

# 创建数据库表
db.connect()
db.create_tables([User], safe=True)
db.close()

# 创建Sanic应用程序
app = Sanic("DataModelSanicApp")

@app.exception(ServerError)
async def handle_server_error(request, exception):
    """服务器错误处理"""
    return json({'error': str(exception)}, status=500)

@app.exception(NotFound)
async def handle_not_found(request, exception):
    """未找到错误处理"""
    return json({'error': 'Resource not found'}, status=404)

@app.route('/users', methods=['GET'])
async def get_users(request):
    """获取用户列表"""
    try:
        users = User.select()
        return json([dict(user) for user in users])
    except Exception as e:
        raise ServerError(f"Error retrieving users: {e}")

@app.route('/users/<int:user_id>', methods=['GET'])
async def get_user(request, user_id):
    """根据ID获取单个用户"""
    try:
        user = User.get(User.id == user_id)
        return json(dict(user))
    except User.DoesNotExist:
        raise NotFound('User not found')
    except Exception as e:
        raise ServerError(f"Error retrieving user: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)