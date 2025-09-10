# 代码生成时间: 2025-09-10 16:04:19
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, abort
from sanic.response import json as sanic_json

# Inventory management application
app = Sanic("InventoryManagement")

# In-memory inventory storage
inventory = {}

# Helper function to initialize inventory
def initialize_inventory():
    inventory.clear()
    inventory["items"] = {
        "001": {"name": "Apple", "quantity": 50},
        "002": {"name": "Banana", "quantity": 30},
        "003": {"name": "Cherry", "quantity": 20}
    }

# Get all inventory items
@app.route("/items", methods=["GET"])
async def get_items(request):
    """
    Retrieve a list of all inventory items.
    """
    return sanic_json(inventory["items"])

# Get a specific inventory item by ID
@app.route("/items/<item_id>", methods=["GET"])
async def get_item(request, item_id):
    """
    Retrieve a specific inventory item by its ID.
    """
    if item_id in inventory["items"]:
        return sanic_json(inventory["items"][item_id])
    else:
        abort(404, "Item not found")

# Add or update an inventory item
@app.route("/items", methods=["POST"])
async def add_or_update_item(request):
    """
    Add or update an inventory item.
    """
    data = request.json
    if "id" not in data or "name" not in data or "quantity" not in data:
        abort(400, "Invalid item data")
    
    inventory["items"][data["id"]] = {
        "name": data["name"],
        "quantity": data["quantity"]
    }
    return sanic_json(inventory["items"][data["id"]])

# Delete an inventory item
@app.route("/items/<item_id>", methods=["DELETE"])
async def delete_item(request, item_id):
    """
    Delete a specific inventory item by its ID.
    """
    if item_id in inventory["items"]:
        del inventory["items"][item_id]
        return response.text("Item deleted")
    else:
        abort(404, "Item not found")

# Error handler for 404 errors
@app.exception(404)
async def not_found(request, exception):
    return response.json({"error": "Not Found"}, status=404)

# Error handler for 400 errors
@app.exception(400)
async def bad_request(request, exception):
    return response.json({"error": "Bad Request"}, status=400)

# Error handler for ServerError
@app.exception(ServerError)
async def server_error(request, exception):
    return response.json({"error": "Internal Server Error"}, status=500)

if __name__ == "__main__":
    initialize_inventory()
    app.run(host="0.0.0.0", port=8000)