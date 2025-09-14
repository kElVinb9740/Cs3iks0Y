# 代码生成时间: 2025-09-14 08:25:29
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
import subprocess
import psutil
import os
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Sanic('process_manager')

# 启动一个进程
@app.route('/run/<process_name>', methods=['GET'])
async def run_process(request, process_name):
    try:
        # 检查进程名是否合法
        if not process_name.isalnum():
            return response.json({'error': 'Invalid process name'}, status=400)

        # 启动进程
        process = subprocess.Popen(process_name, shell=True)
        return response.json({'message': f'Process {process_name} started with PID {process.pid}'})
    except Exception as e:
        logger.error(f'Failed to start process {process_name}: {e}')
        return response.json({'error': str(e)}, status=500)

# 终止一个进程
@app.route('/stop/<pid>', methods=['GET'])
async def stop_process(request, pid):
    try:
        # 检查PID是否为数字
        if not pid.isdigit():
            return response.json({'error': 'Invalid PID'}, status=400)

        # 终止进程
        process = psutil.Process(int(pid))
        if process.is_running():
            process.terminate()
            return response.json({'message': f'Process {pid} terminated'})
        else:
            return response.json({'error': f'Process {pid} is not running'})
    except Exception as e:
        logger.error(f'Failed to stop process {pid}: {e}')
        return response.json({'error': str(e)}, status=500)

# 获取进程列表
@app.route('/list', methods=['GET'])
async def list_processes(request):
    try:
        # 获取所有进程
        processes = [p.info for p in psutil.process_iter(['pid', 'name', 'status', 'create_time', 'memory_info'])]
        return response.json({'processes': processes})
    except Exception as e:
        logger.error('Failed to list processes: {e}')
        return response.json({'error': str(e)}, status=500)

# 获取特定进程详情
@app.route('/info/<pid>', methods=['GET'])
async def get_process_info(request, pid):
    try:
        # 检查PID是否为数字
        if not pid.isdigit():
            return response.json({'error': 'Invalid PID'}, status=400)

        # 获取进程详情
        process = psutil.Process(int(pid))
        process_info = process.as_dict(attrs=['pid', 'name', 'status', 'create_time', 'memory_info'])
        return response.json({'process_info': process_info})
    except Exception as e:
        logger.error(f'Failed to get process info for {pid}: {e}')
        return response.json({'error': str(e)}, status=500)

# 启动Sanic服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=False)