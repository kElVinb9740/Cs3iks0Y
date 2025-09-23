# 代码生成时间: 2025-09-23 18:06:39
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import ServerError, ServerErrorMiddleware

# Define a custom middleware to handle server errors
class JSONErrorMiddleware(ServerErrorMiddleware):
    async def error(self, request, exception):
        return response.json({
            "error": str(exception)
        }, status=exception.status_code)

app = Sanic("ThemeSwitcherApp")

# Define a simple in-memory store for themes
themes_store = {
    "light": "Light theme",
    "dark": "Dark theme"
}

# Default theme
default_theme = "light"

# Route to switch themes
@app.route("/switch_theme", methods=["POST"])
async def switch_theme(request: Request):
    try:
        # Retrieve the theme from the request body
        data = request.json
        new_theme = data.get("theme")

        # Check if the new theme is valid
        if new_theme not in themes_store:
            raise ValueError("Invalid theme provided.")

        # Update the default theme
        global default_theme
        default_theme = new_theme

        # Return the updated theme
        return response.json({
            "message": "Theme switched successfully",
            "current_theme": default_theme
        })
    except ValueError as ve:
        # Return a 400 bad request error with a message
        return response.json({
            "error": str(ve)
        }, status=400)
    except Exception as e:
        # Propagate any other exceptions
        raise ServerError(str(e), status_code=500)

# Route to get the current theme
@app.route("/get_theme", methods=["GET"])
async def get_current_theme(request: Request):
    # Return the current theme
    return response.json({
        "current_theme": default_theme
    })

# Run the Sanic app
if __name__ == "__main__":
    app.static("/static", os.path.join(os.getcwd(), "static"))
    app.add_middleware(JSONErrorMiddleware)
    app.run(host="0.0.0.0", port=8000, auto_reload=False)
