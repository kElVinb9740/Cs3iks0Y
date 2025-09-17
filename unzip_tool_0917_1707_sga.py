# 代码生成时间: 2025-09-17 17:07:17
import zipfile
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import ServerError, NotFound

# 定义一个Sanic app
app = Sanic("Unzip Tool")

# 函数：解压文件
def unzip_file(zip_path, extract_to):
    """
    解压ZIP文件到指定目录
    :param zip_path: ZIP文件路径
    :param extract_to: 目标解压目录
    :return: None
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile:
        raise ServerError("ZIP文件损坏")
    except FileNotFoundError:
        raise NotFound("文件不存在")
    except Exception as e:
        raise ServerError(f"解压过程中发生错误: {e}")

# Sanic路由：解压文件
@app.route('/api/unzip', methods=['POST'])
async def unzip_file_handler(request: Request):
    """
    接收ZIP文件并将其解压
    :param request: 请求对象
    :return: JSON响应
    """
    try:
        # 获取上传的文件
        file = request.files.get('file')
        if not file:
            return response.json({'error': '没有上传文件'}, status=400)

        # 获取文件名和解压目录
        file_name = file.name
        zip_path = os.path.join(".", file_name)
        extract_to = "./extracted"

        # 保存文件
        with open(zip_path, 'wb') as f:
            f.write(file.body)

        # 解压文件
        unzip_file(zip_path, extract_to)

        # 返回成功响应
        return response.json({'message': '解压成功'}, status=200)
    except ServerError as e:
        return response.json({'error': str(e)}, status=500)
    except NotFound as e:
        return response.json({'error': str(e)}, status=404)
    except Exception as e:
        return response.json({'error': f'未知错误: {e}'}, status=500)

# 运行Sanic app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)