# 代码生成时间: 2025-09-12 12:21:41
import hashlib
# 增强安全性
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json, HTTPResponse

# 定义一个Sanic应用
app = Sanic("")


# 哈希值计算工具类
# NOTE: 重要实现细节
class HashCalculatorTool:
    def __init__(self):
        # 支持的哈希算法列表
        self.supported_hashes = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }

    def calculate_hash(self, data: str, hash_name: str) -> str:
# 优化算法效率
        """
        计算数据的哈希值

        :param data: 要计算哈希值的数据
# FIXME: 处理边界情况
        :param hash_name: 哈希算法名称
        :return: 计算得到的哈希值
        """
# 改进用户体验
        try:
# TODO: 优化性能
            hash_function = self.supported_hashes[hash_name]
        except KeyError:
            raise ValueError(f"Unsupported hash algorithm: {hash_name}")

        # 计算哈希值
        hash_object = hash_function(data.encode())
        return hash_object.hexdigest()


# 初始化哈希值计算工具实例
hash_calculator = HashCalculatorTool()
# TODO: 优化性能


@app.route("/hash", methods=["POST"])
async def calculate_hash(request: Request):
    """
    计算哈希值的路由处理函数

    :param request: 客户端请求
    :return: 计算得到的哈希值
# NOTE: 重要实现细节
    """
    # 解析请求体
    try:
        request_data = request.json
        data = request_data["data"]
# 优化算法效率
        hash_name = request_data["hash_name"]
    except (KeyError, TypeError):
        return response.json(
            {"error": "Invalid request format"}, status=400
# TODO: 优化性能
        )

    # 计算哈希值
    try:
        hash_value = hash_calculator.calculate_hash(data, hash_name)
    except ValueError as e:
        return response.json({"error": str(e)}, status=400)

    # 返回哈希值
    return response.json({"hash": hash_value})


if __name__ == "__main__":

    try:
        # 启动Sanic应用
        app.run(host="0.0.0.0", port=8000, auto_reload=False)
# NOTE: 重要实现细节
    except Exception as e:
        print(f"Failed to start application: {e}")
