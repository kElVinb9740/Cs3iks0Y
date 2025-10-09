# 代码生成时间: 2025-10-10 03:10:21
import json
from sanic import Sanic, response, exceptions
from sanic.request import Request
from sanic.response import text


# 定义富文本编辑器服务
class RichTextEditorService:
    def __init__(self):
        # 初始化编辑器状态
        self.content = ""

    def update_content(self, new_content):
        """更新编辑器内容"""
        self.content = new_content
        return {
            "status": "success",
            "message": "Content updated successfully",
            "content": self.content
        }

    def get_content(self):
        """获取当前编辑器内容"""
        return {
            "status": "success",
            "message": "Content retrieved successfully",
            "content": self.content
        }


# 创建Sanic应用
app = Sanic("RichTextEditor")

# 实例化富文本编辑器服务
text_editor_service = RichTextEditorService()


# 定义更新编辑器内容的路由
@app.post("/update_content")
async def update_content(request: Request):
    try:
        content = request.json.get("content")
        if not content:
            raise exceptions.bad_request("Content is required")
        response_data = text_editor_service.update_content(content)
        return response.json(response_data)
    except (json.JSONDecodeError, exceptions.bad_request) as e:
        return response.json(
            {
                "status": "error",
                "message": str(e)
            },
            status=400
        )

# 定义获取编辑器内容的路由
@app.get("/get_content")
async def get_content(request: Request):
    try:
        response_data = text_editor_service.get_content()
        return response.json(response_data)
    except Exception as e:
        return response.json(
            {
                "status": "error",
                "message": str(e)
            },
            status=500
        )


# 运行Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)