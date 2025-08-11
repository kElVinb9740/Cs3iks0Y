# 代码生成时间: 2025-08-12 02:48:17
import jinja2
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import json as sanic_json
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化模板环境
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='./templates'))

app = Sanic("TestReportGenerator")

\@app.exception(ServerError)
async def handle_exception(request: Request, exception: Exception):
    """错误处理中间件，记录异常并返回错误信息"""
    logger.error(f"Unhandled exception: {exception}")
    return sanic_json({'error': str(exception)}, status=500)

\@app.route("/report", methods=["GET"])
async def generate_report(request: Request):
    """生成测试报告的接口"""
    try:
        # 模拟测试数据
        test_data = {
            'total_tests': 100,
            'passed_tests': 90,
            'failed_tests': 10,
            'skipped_tests': 0,
        }

        # 渲染模板
        template = env.get_template("report_template.html")
        report_html = template.render(test_data)

        # 将HTML内容写入文件
        with open("test_report.html", "w") as report_file:
            report_file.write(report_html)

        # 返回文件路径
        return response.file("test_report.html")
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return sanic_json({'error': 'Failed to generate report'}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
