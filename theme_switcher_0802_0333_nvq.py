# 代码生成时间: 2025-08-02 03:33:01
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError, NotFound
from sanic.handlers import ErrorHandler
from sanic.config import LOGGING_CONFIG_DEFAULTS

# Define a custom error handler
class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception):
        return json({'error': str(exception)}, status=500)

# Initialize the Sanic app
app = Sanic('ThemeSwitcherApp')

# Theme settings
theme_settings = {
    'light': 'Light Theme',
    'dark': 'Dark Theme',
    'system': 'System Theme'
}

# Save the current theme in the session
@app.listener('before_server_start')
async def setup_theme(app, loop):
    # Initialize the theme
    app.theme = 'light'  # Default theme

# Route to switch themes
@app.route('/switch-theme/<theme_name>', methods=['GET'])
async def switch_theme(request, theme_name):
    """
    Switch the theme based on the theme_name parameter.
    The theme_name should be one of the keys in theme_settings.
    If the theme_name is not valid, return a 404 error.
    """
    try:
        if theme_name in theme_settings:
            app.theme = theme_name
            return json({'message': 'Theme switched to ' + theme_settings[theme_name]}, status=200)
        else:
            raise NotFound('Theme not found')
    except NotFound as e:
        return json({'error': str(e)}, status=404)
    except Exception as e:
        raise ServerError('An error occurred', e)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, error_handler=CustomErrorHandler())
