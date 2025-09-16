# 代码生成时间: 2025-09-16 16:36:38
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.views import CompositionView
from sanic_openapi import swagger_blueprint, openapi_blueprint
import json
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Initialize Sanic app
app = Sanic(__name__)

# Define the Swagger documentation
api_blueprint = swagger_blueprint(app)
app.register_blueprint(api_blueprint, url_prefix='/swagger')
openapi_blueprint(app, '/api')

# This view handles GET requests to generate an interactive chart
@app.route('/chart', methods=['GET'])
async def chart(request):
    # Check if the request contains required parameters
    if 'data' not in request.args:
        raise ServerError('Missing required parameter: data', status_code=400)

    try:
        # Get the data from the request and parse it as JSON
        data = json.loads(request.args['data'][0])
    except json.JSONDecodeError:
        raise ServerError('Invalid JSON data provided', status_code=400)

    # Generate the chart
    try:
        fig, ax = plt.subplots()
        x = np.arange(len(data['points']))
        ax.plot(x, data['points'], label=data['label'])
        ax.set_title(data['title'])
        ax.set_xlabel(data['xlabel'])
        ax.set_ylabel(data['ylabel'])
        ax.legend()
    except KeyError as e:
        raise ServerError(f'Missing data for chart generation: {e}', status_code=400)

    # Save the chart to a BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the image to base64 and return it as a response
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return response.json({ 'image': f"data:image/png;base64,{img_base64}" })

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=2)

"""
Swagger Documentation
"""
swagger = {
    '/swagger/': {
        'get': {
            'summary': 'Swagger API Docs',
            'responses': {
                200: {
                    'description': 'Api Documentation'
                }
            }
        }
    },
    '/chart': {
        'get': {
            'summary': 'Generate an interactive chart',
            'description': 'Generates an interactive chart based on the provided data',
            'parameters': [
                {
                    'name': 'data',
                    'in': 'query',
                    'description': 'Data for chart generation',
                    'required': True,
                    'schema': {
                        'type': 'string',
                        'format': 'json'
                    }
                }
            ],
            'responses': {
                200: {
                    'description': 'Image of the generated chart',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'image': {
                                'type': 'string',
                                'format': 'data uri'
                            }
                        }
                    }
                }
            }
        }
    }
}
