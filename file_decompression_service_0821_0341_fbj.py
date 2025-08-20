# 代码生成时间: 2025-08-21 03:41:00
import zipfile
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import ServerError, ServerNotReady
from sanic.handlers import ErrorHandler
from sanic.log import logger
import tempfile


# Define the Sanic application
app = Sanic("FileDecompressionService")

# Route to handle file uploads and decompression
@app.route("/decompress", methods=["POST"])
async def handle_decompress(request: Request):
    # Check if the request has a file
    if 'file' not in request.files:
        return response.json(
            {
                "error": "No file part in the request"
            },
            status=400
        )

    file = request.files['file']
    if file is None:
        return response.json(
            {
                "error": "No selected file"
            },
            status=400
        )

    try:
        # Create a temporary directory to store the uploaded file
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Save the uploaded file to a temporary location
            tmp_file_path = os.path.join(tmpdirname, file.filename)
            with open(tmp_file_path, 'wb') as tmp_file:
                tmp_file.write(file.body)

            # Decompress the file
            if file.filename.endswith('.zip'):
                with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                    files = [f for f in os.listdir(tmpdirname) if os.path.isfile(os.path.join(tmpdirname, f))]
                    
                    # Return the list of extracted file names
                    return response.json(files)
            else:
                return response.json(
                    {
                        "error": "Unsupported file format"
                    },
                    status=400
                )
    except Exception as e:
        logger.error(f"Error occurred during decompression: {str(e)}")
        return response.json(
            {
                "error": "An error occurred during decompression"
            },
            status=500
        )

# Error handler for Sanic
class MyErrorHandler(ErrorHandler):
    def default(self, exception: ServerError, request: Request):
        if exception.status_code == 500:
            return response.json(
                {
                    "error": "Internal Server Error"
                },
                status=500
            )
        return response.json(
            {
                "error": str(exception)
            },
            status=exception.status_code
        )

# Register the error handler
app.error_handler = MyErrorHandler(
    app,
    type(ServerError("", 500))
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
