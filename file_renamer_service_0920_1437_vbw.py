# 代码生成时间: 2025-09-20 14:37:34
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import ServerError, Unauthorized

# 文件重命名服务类
class FileRenamerService:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def rename_files(self, paths, new_names):
        """批量重命名文件函数

        Args:
            paths (list): 原始文件路径列表
            new_names (list): 新文件名列表
        Returns:
            list: 重命名结果列表
        """
        if len(paths) != len(new_names):
            raise ValueError("文件路径和新文件名的数量必须匹配")

        results = []
        for path, new_name in zip(paths, new_names):
            full_path = os.path.join(self.root_dir, path)
            new_full_path = os.path.join(self.root_dir, new_name)

            if not os.path.isfile(full_path):
                results.append({"path": path, "status": "error", "message": "文件不存在"})
                continue

            try:
                os.rename(full_path, new_full_path)
                results.append({"path": path, "status": "success", "message": "文件重命名成功"})
            except OSError as e:
                results.append({"path": path, "status": "error", "message": str(e)})

        return results

# 创建Sanic应用
app = Sanic("FileRenamerService")

# 定义路由处理批量文件重命名请求
@app.route("/rename", methods=["POST"])
async def rename_files(request: Request):
    # 解析请求体中的JSON数据
    try:
        data = request.json
        paths = data.get("paths", [])
        new_names = data.get("new_names", [])
    except Exception as e:
        return response.json(
            {
                "status": "error",
                "message": "解析请求数据失败",
                "error": str(e),
            },
            status=400,
        )

    # 调用文件重命名服务
    try:
        service = FileRenamerService(root_dir="./files")
        results = service.rename_files(paths, new_names)
    except Exception as e:
        return response.json(
            {
                "status": "error",
                "message": "文件重命名失败",
                "error": str(e),
            },
            status=500,
        )

    # 返回重命名结果
    return response.json(
        {
            "status": "success",
            "results": results,
        },
        status=200,
    )

# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)