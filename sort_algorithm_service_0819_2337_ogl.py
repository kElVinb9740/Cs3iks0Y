# 代码生成时间: 2025-08-19 23:37:45
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.request import Request
from sanic.response import json

# 创建Sanic应用
app = Sanic("SortAlgorithmService")

# 定义全局变量，存储排序算法状态
SORT_STATE = {}

# 定义排序算法函数
def bubble_sort(arr):
    """冒泡排序算法实现
    Args:
        arr (list): 需要排序的列表
    Returns:
        sorted_list (list): 排序后的列表
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr):
    """插入排序算法实现
    Args:
        arr (list): 需要排序的列表
    Returns:
        sorted_list (list): 排序后的列表
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# 定义Sanic路由
@app.route('/api/sort', methods=['POST'])
async def sort_request(request: Request):
    """处理排序请求"""
    try:
        # 获取请求体中的排序算法和待排序的数组
        sort_algorithm = request.json.get('algorithm')
        arr = request.json.get('array')

        # 错误处理：检查排序算法是否存在
        if sort_algorithm not in ['bubble', 'insertion']:
            raise NotFound("Sort algorithm not found")

        # 错误处理：检查待排序数组是否合法
        if not isinstance(arr, list):
            raise ServerError("Invalid array format")

        # 根据排序算法进行排序
        if sort_algorithm == 'bubble':
            sorted_arr = bubble_sort(arr.copy())
        elif sort_algorithm == 'insertion':
            sorted_arr = insertion_sort(arr.copy())

        # 返回排序结果
        return response.json({'sorted_array': sorted_arr})
    except (ServerError, NotFound) as e:
        # 返回错误信息
        return response.json({'error': str(e)}, status=e.status_code)
    except Exception as e:
        # 处理未预期的异常
        return response.json({'error': 'Internal Server Error'}, status=500)

# 定义启动服务器的函数
def run_server():
    """启动Sanic服务器"""
    app.run(host='0.0.0.0', port=8000, workers=1)

# 检查是否直接运行该脚本
if __name__ == '__main__':
    run_server()