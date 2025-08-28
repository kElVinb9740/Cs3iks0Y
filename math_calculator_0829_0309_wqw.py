# 代码生成时间: 2025-08-29 03:09:13
import math
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.request import Request
from sanic.response import json

# 创建Sanic应用实例
def create_math_calculator_app():
    app = Sanic("MathCalculatorApp")
    
    # 定义数学计算工具集路由
    @app.route("/add", methods=["GET"])
    async def add(request: Request):
        # 获取查询参数
        a = request.args.get("a", type=float)
        b = request.args.get("b", type=float)
        
        # 检查参数是否存在和类型是否正确
        if a is None or b is None:
            raise NotFound("Missing required parameters")
        
        # 执行加法运算
        result = a + b
        return json({
            "result": result
        })
    
    @app.route("/subtract", methods=["GET"])
    async def subtract(request: Request):
        a = request.args.get("a", type=float)
        b = request.args.get("b", type=float)
        
        if a is None or b is None:
            raise NotFound("Missing required parameters")
        
        result = a - b
        return json({
            "result": result
        })
    
    @app.route("/multiply", methods=["GET"])
    async def multiply(request: Request):
        a = request.args.get("a", type=float)
        b = request.args.get("b", type=float)
        
        if a is None or b is None:
            raise NotFound("Missing required parameters")
        
        result = a * b
        return json({
            "result": result
        })
    
    @app.route("/divide", methods=["GET"])
    async def divide(request: Request):
        a = request.args.get("a", type=float)
        b = request.args.get("b", type=float)
        
        if a is None or b is None or b == 0:
            raise NotFound("Missing required parameters or division by zero")
        
        result = a / b
        return json({
            "result": result
        })
    
    @app.route("/square_root", methods=["GET"])
    async def square_root(request: Request):
        number = request.args.get("number", type=float)
        
        if number is None or number < 0:
            raise NotFound("Missing required parameters or negative number")
        
        result = math.sqrt(number)
        return json({
            "result": result
        })
    
    return app

# 运行Sanic应用实例
if __name__ == "__main__":
    app = create_math_calculator_app()
    app.run(host="0.0.0.0", port=8000, workers=1)