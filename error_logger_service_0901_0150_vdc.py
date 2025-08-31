# 代码生成时间: 2025-09-01 01:50:07
import logging
from sanic import Sanic
from sanic.response import json
from sanic.log import logger as sanic_logger
import os

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 错误日志文件路径
ERROR_LOG_FILE_PATH = 'error_log.txt'

app = Sanic('error_logger_service')

# 错误处理器
@app.exception
async def handle_exception(request, exception):
    logger.error(f'Exception: {exception}')
    # 将错误写入日志文件
    with open(ERROR_LOG_FILE_PATH, 'a') as error_log_file:
        error_log_file.write(f'{exception}
')
    return json({'error': 'Internal Server Error'}, status=500)

# 测试路由，用于触发错误
@app.route('/test', methods=['GET'])
async def test(request):
    # 故意触发一个错误
    raise ValueError('Test error')

# 启动服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
