# 代码生成时间: 2025-08-18 10:11:21
import os
import csv
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError, ServerError
from sanic.views import CompositionView

# 定义一个函数来处理CSV文件
def process_csv_file(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            data = [headers]  # 包含表头的数据列表
            for row in reader:
                data.append(row)
            return data
    except Exception as e:
        raise ServerError(f"Failed to process CSV file: {e}")

# 创建一个Sanic应用
app = Sanic("CSV Batch Processor", auto_reload=False)

# 定义一个路由来处理上传的CSV文件
@app.route("/process", methods=["POST"])
async def process_files(request: Request):
    files = request.files.getall("files")
    if not files:
        return response.json({"error": "No files provided"}, status=400)

    results = []
    for file in files:
        file_path = file.name
        if not file_path.endswith(".csv"):
            return response.json({"error": f"{file_path} is not a CSV file"}, status=400)

        try:
            result = process_csv_file(file.file)
            results.append(result)
        except ServerError as e:
            results.append(str(e))

    return response.json(results)

# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, auto_reload=False)