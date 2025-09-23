# 代码生成时间: 2025-09-23 11:22:07
import asyncio
from sanic import Sanic
from sanic.response import json, text
from alembic.config import Config
from alembic import command
from alembic.util import CommandError

# 初始化Sanic应用
app = Sanic('DatabaseMigrationTool')

# 配置Alembic
def get_alembic_config():
    config = Config("alembic.ini")
    return config

# 异步运行Alembic命令
async def async_alembic_command(command_name):
    loop = asyncio.get_running_loop()
    try:
        config = get_alembic_config()
        command_result = await loop.run_in_executor(None, lambda: command.revision, config, '-autogenerate' if command_name == 'upgrade' else command_name)
        return {'status': 'success', 'message': 'Migration completed successfully', 'result': command_result}
    except CommandError as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        return {'status': 'error', 'message': 'An unexpected error occurred', 'error': str(e)}

# 迁移工具接口 - 升级数据库
@app.route('/migrate/upgrade', methods=['POST'])
async def migrate_upgrade(request):
    result = await async_alembic_command('upgrade')
    return json(result)

# 迁移工具接口 - 降级数据库
@app.route('/migrate/downgrade', methods=['POST'])
async def migrate_downgrade(request):
    result = await async_alembic_command('downgrade')
    return json(result)

# 迁移工具接口 - 自动生成迁移脚本
@app.route('/migrate/generate', methods=['POST'])
async def migrate_generate(request):
    result = await async_alembic_command('revision')
    return json(result)

# 程序入口点
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=False)
