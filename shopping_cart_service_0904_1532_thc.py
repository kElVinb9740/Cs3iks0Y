# 代码生成时间: 2025-09-04 15:32:04
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound, abort

# 定义一个简单的购物车类
class ShoppingCart:
    def __init__(self):
        # 初始化购物车，使用字典来存储商品ID和数量
        self.items = {}

    def add_item(self, item_id, quantity):
        # 向购物车添加商品
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity

    def remove_item(self, item_id, quantity):
        # 从购物车移除商品
        if item_id in self.items:
            if self.items[item_id] > quantity:
                self.items[item_id] -= quantity
            else:
                del self.items[item_id]
        else:
            raise NotFound("Item not found in cart")

    def get_cart(self):
        # 获取购物车内容
        return self.items

    def clear_cart(self):
        # 清空购物车
        self.items = {}

# 创建Sanic应用
app = Sanic("Shopping Cart Service")

# 购物车实例
cart = ShoppingCart()

# 路由：添加商品到购物车
@app.route("/add_item", methods=["POST"])
async def add_item(request):
    # 解析请求体
    data = request.json
    item_id = data.get("item_id")
    quantity = data.get("quantity")

    # 检查参数
    if not item_id or not quantity:
        abort(400, "Missing item_id or quantity")

    try:
        # 添加商品到购物车
        cart.add_item(item_id, quantity)
        return response.json({"message": "Item added to cart"})
    except Exception as e:
        raise ServerError("Error adding item to cart", e)

# 路由：从购物车移除商品
@app.route("/remove_item", methods=["POST"])
async def remove_item(request):
    # 解析请求体
    data = request.json
    item_id = data.get("item_id")
    quantity = data.get("quantity")

    # 检查参数
    if not item_id or not quantity:
        abort(400, "Missing item_id or quantity")

    try:
        # 从购物车移除商品
        cart.remove_item(item_id, quantity)
        return response.json({"message": "Item removed from cart"})
    except NotFound as e:
        return response.json({"error": str(e)}, status=404)
    except Exception as e:
        raise ServerError("Error removing item from cart", e)

# 路由：获取购物车内容
@app.route("/get_cart", methods=["GET"])
async def get_cart(request):
    try:
        # 获取购物车内容
        cart_items = cart.get_cart()
        return response.json(cart_items)
    except Exception as e:
        raise ServerError("Error getting cart", e)

# 路由：清空购物车
@app.route("/clear_cart", methods=["POST"])
async def clear_cart(request):
    try:
        # 清空购物车
        cart.clear_cart()
        return response.json({"message": "Cart cleared"})
    except Exception as e:
        raise ServerError("Error clearing cart", e)

# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)