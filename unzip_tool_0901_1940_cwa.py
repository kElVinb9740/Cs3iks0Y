# 代码生成时间: 2025-09-01 19:40:37
import os
import zipfile
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import ServerError, NotFound

# 定义我们的Sanic应用
app = Sanic("UnzipTool")

# 路由处理函数：解压ZIP文件
@app.route("/unzip", methods=["POST"])
async def unzip_file(request: Request):
    # 获取上传的文件
    file = request.files.get("file")
    if not file:
        return response.json({"error": "No file provided"}, status=400)

    # 保存上传的文件到临时目录
    temp_path = "temp.zip"
    with open(temp_path, 'wb') as f:
        f.write(file.body)

    try:
        # 解压文件
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            zip_ref.extractall("extracted_files")
        # 返回成功的响应
        return response.json({"message": "File extracted successfully"})
    except zipfile.BadZipFile:
        # 处理损坏的ZIP文件
        return response.json({"error": "The file is not a valid zip file"}, status=400)
    except Exception as e:
        # 处理其他异常
        return response.json({"error": str(e)}, status=500)
    finally:
        # 清理临时文件
        os.remove(temp_path)

# 启动Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)