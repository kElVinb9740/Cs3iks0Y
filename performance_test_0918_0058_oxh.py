# 代码生成时间: 2025-09-18 00:58:47
import asyncio
import random
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError
from urllib.parse import urlparse, parse_qs

# 定义全局变量，用于存储请求时间
REQUEST_TIMES = []

# 创建Sanic应用
app = Sanic('PerformanceTestApp')

# 定义一个简单的性能测试路由
@app.route('/test', methods=['GET', 'POST'])
async def performance_test(request: Request):
    # 记录请求开始时间
    start_time = asyncio.get_event_loop().time()
    
    # 模拟一些计算工作
    await asyncio.sleep(random.uniform(0.1, 0.5))
    
    # 记录请求结束时间
    end_time = asyncio.get_event_loop().time()
    
    # 计算请求处理时间并存储
    REQUEST_TIMES.append(end_time - start_time)
    
    # 返回请求处理时间
    return response.json({'request_time': end_time - start_time})

# 定义一个路由，用于获取平均请求处理时间
@app.route('/average_time', methods=['GET'])
async def average_request_time(request: Request):
    # 检查是否有请求时间数据
    if REQUEST_TIMES:
        # 计算平均请求时间
        average_time = sum(REQUEST_TIMES) / len(REQUEST_TIMES)
        return response.json({'average_request_time': average_time})
    else:
        # 如果没有请求时间数据，返回错误信息
        return response.json({'error': 'No request times available'}, status=204)

# 定义一个路由，用于重置请求时间数据
@app.route('/reset', methods=['GET'])
async def reset_request_times(request: Request):
    global REQUEST_TIMES
    REQUEST_TIMES = []
    return response.json({'message': 'Request times have been reset'})

# 定义一个错误处理器
@app.exception(ServerError)
async def handle_server_error(request: Request, exception: ServerError):
    return response.json({'error': 'Internal Server Error'}, status=500)

# 定义一个启动服务器的函数
def run_server():
    # 运行Sanic应用
    app.run(host='0.0.0.0', port=8000, workers=1)

# 如果直接运行这个脚本，启动服务器
if __name__ == '__main__':
    run_server()
