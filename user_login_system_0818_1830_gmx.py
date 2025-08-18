# 代码生成时间: 2025-08-18 18:30:49
import json
from sanic import Sanic
from sanic.response import text, json
from sanic.exceptions import ServerError, abort
from sanic.exceptions import Unauthorized
from sanic_jwt import Initialize, JWTManager

# 用户登录验证系统
app = Sanic("UserLoginSystem")

# 配置JWT
app.config.API_SECRET_KEY = "your_secret_key"

# 初始化JWT
jwt = Initialize(app)

# 假设的用户数据库
USER_DATABASE = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"}
}

# 登录路由
@app.route("/login", methods=["POST"])
async def login(request):
    try:
        # 获取请求体
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # 验证用户名和密码
        if not username or not password:
            raise Unauthorized("Username and Password are required")

        user = USER_DATABASE.get(username)
        if not user or user["password"] != password:
            raise Unauthorized("Invalid Credentials")

        # 创建JWT token
        payload = {"username": username}
        token = jwt.encode(payload)

        # 返回JWT token
        return json({
            "token": token,
            "message": "Login successful"
        })
    except Unauthorized as e:
        return json({"error": str(e)}, status=401)
    except ServerError as e:
        return text("Internal Server Error", status=500)
    except Exception as e:
        return text("An error occurred", status=500)

# 排除路由外的任何其他路由
@app.route("/<path:path>", methods=["*"])
async def not_found(request, path):
    return abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)