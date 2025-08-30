# 代码生成时间: 2025-08-31 01:17:52
import sanic
from sanic.response import json, file
from PIL import Image
import os

# 定义一个常量存放图片的原始路径和处理后的图片存放路径
ORIGINAL_IMAGE_DIR = 'original_images/'
RESIZED_IMAGE_DIR = 'resized_images/'

app = sanic.Sanic('ImageResizer')

# 确保存放图片的目录存在
if not os.path.exists(ORIGINAL_IMAGE_DIR):
    os.makedirs(ORIGINAL_IMAGE_DIR)
if not os.path.exists(RESIZED_IMAGE_DIR):
    os.makedirs(RESIZED_IMAGE_DIR)

@app.route('/upload', methods=['POST'])
async def upload_image(request):
    """
    处理上传的图片，并将图片保存到服务器。
    """
    try:
        # 获取上传的文件
        file = request.files.get('file')
        if not file:
            return json({'error': 'No file provided'}, status=400)

        # 保存图片到指定目录
        file_path = os.path.join(ORIGINAL_IMAGE_DIR, file.filename)
        with open(file_path, 'wb') as f:
            f.write(file.body)

        return json({'message': 'Image uploaded successfully'}, status=200)
    except Exception as e:
        return json({'error': str(e)}, status=500)

@app.route('/resize/<width:int>/<height:int>', methods=['GET'])
async def resize_image(request, width, height):
    """
    根据提供的宽度和高度，对上传的图片进行尺寸调整。
    """
    try:
        # 遍历原始图片目录下的图片文件
        for filename in os.listdir(ORIGINAL_IMAGE_DIR):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                # 打开图片文件
                original_image_path = os.path.join(ORIGINAL_IMAGE_DIR, filename)
                resized_image_path = os.path.join(RESIZED_IMAGE_DIR, filename)
                with Image.open(original_image_path) as img:
                    # 调整图片尺寸
                    img = img.resize((width, height))
                    img.save(resized_image_path)

        return json({'message': 'Images resized successfully'}, status=200)
    except Exception as e:
        return json({'error': str(e)}, status=500)

@app.route('/download/<filename>', methods=['GET'])
async def download_image(request, filename):
    """
    下载经过尺寸调整后的图片。
    """
    try:
        # 检查文件是否存在
        file_path = os.path.join(RESIZED_IMAGE_DIR, filename)
        if os.path.exists(file_path):
            return file(file_path)
        else:
            return json({'error': 'File not found'}, status=404)
    except Exception as e:
        return json({'error': str(e)}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)