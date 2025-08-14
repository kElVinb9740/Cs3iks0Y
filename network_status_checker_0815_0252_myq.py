# 代码生成时间: 2025-08-15 02:52:32
import asyncio
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError, NotFound
import requests
import time

def check_connection(url):
    """
    Check if a URL is reachable and returns the status code.
    
    :param url: The URL to check
    :return: A dictionary with the connection status and response code
    """
    try:
        response = requests.head(url, timeout=5)
        return {"status": "connected", "code": response.status_code}
    except requests.ConnectionError:
        return {"status": "disconnected", "code": 0}
    except requests.Timeout:
        return {"status": "timeout", "code": 0}
    except requests.RequestException:
        return {"status": "error", "code": 0}

def error_handler(request, exception):
    """
    Log and handle exceptions.
    
    :param request: The request object
    :param exception: The exception that occurred
    :return: A JSON response with a status message
    """
    print(f"An error occurred: {str(exception)}")
    return json({
        "status": "error",
        "message": str(exception)
    }, status=500)

def main():
    """
    Create the Sanic application and define routes.
    """
    app = Sanic("NetworkStatusChecker")
    app.error_handler = error_handler
    """
    Define a route for checking the network status.
    This route accepts a GET request with a URL parameter.
    """
    @app.route("/check", methods=["GET"])
    async def check_status(request):
        # Extract the URL from the query parameters
        url = request.args.get("url")
        if not url:
            return json({
                "status": "error",
                "message": "URL parameter is missing"
            }, status=400)
        # Check the connection status and return the result
        status = check_connection(url)
        return json(status)
    # Run the application
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()