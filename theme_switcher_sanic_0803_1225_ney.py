# 代码生成时间: 2025-08-03 12:25:23
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, abort
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView


# 定义主题切换的视图
class ThemeSwitcherView(HTTPMethodView):
    async def get(self, request: Request):
        """
        GET请求，用于获取当前的主题。
        """
        theme = request.args.get('theme')
        if theme is not None:
            # 设置主题
            theme = theme[0]
            # 这里可以添加代码来保存主题到数据库或配置文件
            request.app.config['THEME'] = theme
            return response.json({'theme': theme})
        else:
            # 获取当前主题
            theme = request.app.config.get('THEME', 'default')
            return response.json({'theme': theme})

    async def post(self, request: Request):
        """
        POST请求，用于设置主题。
        """
        data = request.json
        if 'theme' not in data:
            abort(400, 'Missing theme parameter')
        theme = data['theme']
        # 这里可以添加代码来保存主题到数据库或配置文件
        request.app.config['THEME'] = theme
        return response.json({'theme': theme})


# 创建Sanic应用
app = Sanic('ThemeSwitcherApp')

# 应用配置
app.config['THEME'] = 'default'  # 默认主题

# 注册路由和视图
app.add_route ThemeSwitcherView.as_view(), '/theme'

# 启动Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=True)
