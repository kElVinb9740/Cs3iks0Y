# 代码生成时间: 2025-09-20 19:00:02
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import ServerError, abort


# 定义批量文件重命名工具的Sanic应用
app = Sanic('BatchFileRenamer')


@app.route('/files/rename', methods=['POST'])
async def rename_files(request: Request):
    # 获取请求体中的文件信息和新的文件名
    try:
        files_info = request.json.get('files')
        new_names = request.json.get('new_names')

        # 检查输入数据的有效性
        if not files_info or not new_names or len(files_info) != len(new_names):
            abort(400, 'Invalid input data for file renaming.')

        # 遍历文件信息和新文件名，进行重命名操作
        for file_info, new_name in zip(files_info, new_names):
            file_path = file_info.get('path')
            if not file_path or not os.path.isfile(file_path):
                abort(404, f'File not found: {file_path}')
            try:
                os.rename(file_path, os.path.join(os.path.dirname(file_path), new_name))
            except OSError as e:
                # 处理文件重命名过程中可能出现的异常
                abort(500, f'Error renaming file: {e}')

        # 返回成功的响应
        return response.json({'message': 'Files renamed successfully.'})
    except ServerError as e:
        return response.json({'error': str(e)})
    except Exception as e:
        # 处理未预料到的异常
        return response.json({'error': 'An unexpected error occurred.'}, status=500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
