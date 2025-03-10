import datetime
import uuid

class Order:
    def __init__(self, customer_info, cart_items, total_price):
        self.id = str(uuid.uuid4())
        self.customer_info = customer_info
        self.cart_items = cart_items
        self.total_price = total_price
        self.date = datetime.datetime.now()
        self.status = "Pending"
        
    def to_dict(self):
        return {
            'id': self.id,
            'customer_info': self.customer_info,
            'cart_items': self.cart_items,
            'total_price': self.total_price,
            'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
            'status': self.status
        }


# Mock database for orders
orders_db = {}

def save_order(order):
    orders_db[order.id] = order
    return order.id

def get_order(order_id):
    return orders_db.get(order_id)