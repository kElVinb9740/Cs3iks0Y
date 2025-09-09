# 代码生成时间: 2025-09-09 23:03:06
import os
import sanic
from sanic.response import json
from sanic.exceptions import ServerError
from sanic.request import Request

# 定义批量文件重命名工具
class BatchRenameTool:
    def __init__(self, directory):
        self.directory = directory

    def rename_files(self, rename_map):
        """
        批量重命名文件
        :param rename_map: 旧文件名到新文件名的映射字典
        :return: 重命名结果
        """
        rename_results = []
        for old_name, new_name in rename_map.items():
            try:
                old_path = os.path.join(self.directory, old_name)
                new_path = os.path.join(self.directory, new_name)
                os.rename(old_path, new_path)
                rename_results.append({'old_name': old_name, 'new_name': new_name, 'status': 'success'})
            except OSError as e:
                rename_results.append({'old_name': old_name, 'new_name': new_name, 'status': 'failed', 'error': str(e)})
        return rename_results

# 定义Sanic应用
app = sanic.Sanic('batch_rename_tool')

# 定义批量重命名文件的API
@app.route('/rename_files', methods=['POST'])
async def rename_files(request: Request):
    try:
        rename_map = request.json
        directory = request.json.get('directory', './')
        rename_tool = BatchRenameTool(directory)
        results = rename_tool.rename_files(rename_map)
        return json({'status': 'success', 'results': results})
    except Exception as e:
        raise ServerError('Failed to rename files', body={'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
