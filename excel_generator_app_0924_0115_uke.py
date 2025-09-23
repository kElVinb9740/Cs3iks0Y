# 代码生成时间: 2025-09-24 01:15:41
import asyncio
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse, json
# 增强安全性
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.writer.excel import save_virtual_workbook
import pandas as pd
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the Sanic application
app = Sanic(name='ExcelGeneratorApp')

# Define a route to generate an Excel file
@app.route('/create_excel', methods=['POST'])
async def create_excel(request: Request):
    # Extract JSON data from the request body
    data = request.json
# 添加错误处理

    # Error handling for missing data
    if 'data' not in data:
        return json({'error': 'Missing data in request'}, status=400)

    try:
        # Create a pandas DataFrame from the JSON data
# 扩展功能模块
        df = pd.DataFrame(data['data'])

        # Create an Excel workbook and add a worksheet
        wb = Workbook()
        ws = wb.active

        # Add the DataFrame to the worksheet
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)

        # Save the workbook to a bytes buffer
        output = io.BytesIO()
        save_virtual_workbook(output, wb)
# 扩展功能模块
        output.seek(0)
# 扩展功能模块

        # Return the Excel file as a response
        return response.file(output, filename='generated_excel.xlsx')
    except Exception as e:
        # Log and return an error response if an exception occurs
        logging.error(f'Failed to generate Excel file: {e}')
        return json({'error': 'Failed to generate Excel file'}, status=500)

# Define a route for the application to handle static routes
@app.route('/upload', methods=['GET'])
async def upload(request: Request):
    return response.html('<html><body><h1>Upload an Excel file to generate</h1></body></html>')

# Run the Sanic application
if __name__ == '__main__':
    logging.info('Starting ExcelGeneratorApp...')
    app.run(host='0.0.0.0', port=8000, debug=True)
