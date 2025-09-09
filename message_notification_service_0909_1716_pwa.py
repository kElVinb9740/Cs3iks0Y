# 代码生成时间: 2025-09-09 17:16:39
import asyncio
from sanic import Sanic, response
from sanic.log import logger

# Define a message notification service using the Sanic framework
app = Sanic('MessageNotificationService')

# Define a simple in-memory message storage
message_storage = []

# Define a route for sending notifications
@app.route('/send_notification', methods=['POST'])
async def send_notification(request):
    # Extract the message from the request body
    data = request.json
    if 'message' not in data:
        return response.json({'error': 'Missing message parameter'}, status=400)

    # Validate the message
    if not isinstance(data['message'], str):
        return response.json({'error': 'Invalid message type'}, status=400)

    # Add the message to the storage
    message_storage.append(data['message'])

    # Simulate sending the notification
    logger.info(f'Notification sent: {data['message']}')
    return response.json({'success': True, 'message': 'Notification sent successfully'})

# Define a route for retrieving notifications
@app.route('/get_notifications', methods=['GET'])
async def get_notifications(request):
    # Return the stored notifications
    return response.json({'notifications': message_storage})

# Define a route for clearing notifications
@app.route('/clear_notifications', methods=['POST'])
async def clear_notifications(request):
    global message_storage
    # Clear the message storage
    message_storage.clear()
    return response.json({'success': True, 'message': 'Notifications cleared successfully'})

# Start the Sanic server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)