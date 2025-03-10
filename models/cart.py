class CartItem:
    def __init__(self, product_id, size, color, quantity=1):
        self.product_id = product_id
        self.size = size
        self.color = color
        self.quantity = quantity
        
    def increase_quantity(self, amount=1):
        self.quantity += amount
        
    def decrease_quantity(self, amount=1):
        self.quantity -= amount
        if self.quantity < 1:
            self.quantity = 1
            
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'size': self.size,
            'color': self.color,
            'quantity': self.quantity
        }


class Cart:
    def __init__(self):
        self.items = []
        
    def add_item(self, product_id, size, color, quantity=1):
        # Check if the item already exists in the cart
        for item in self.items:
            if (item.product_id == product_id and 
                item.size == size and 
                item.color == color):
                item.increase_quantity(quantity)
                return
        
        # If not, add a new item
        self.items.append(CartItem(product_id, size, color, quantity))
        
    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
            
    def update_quantity(self, index, quantity):
        if 0 <= index < len(self.items):
            self.items[index].quantity = max(1, quantity)
            
    def get_total_items(self):
        return sum(item.quantity for item in self.items)
    
    def to_dict(self):
        return {
            'items': [item.to_dict() for item in self.items]
        }
        
    def clear(self):
        self.items = []