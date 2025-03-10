class Product:
    def __init__(self, id, name, description, base_price, image):
        self.id = id
        self.name = name
        self.description = description
        self.base_price = base_price
        self.image = image
        self.sizes = ["Small", "Medium", "Large"]
        self.colors = ["Red", "Blue", "Green"]
        
    def get_price_for_size(self, size):
        size_multipliers = {
            "Small": 1.0,
            "Medium": 1.2,
            "Large": 1.5
        }
        return self.base_price * size_multipliers.get(size, 1.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'base_price': self.base_price,
            'image': self.image,
            'sizes': self.sizes,
            'colors': self.colors
        }


# Mock database of products
products_db = {
    1: Product(
        id=1,
        name="SmartBooks: Python Programming",
        description="A comprehensive guide to Python programming with practical examples.",
        base_price=19.99,
        image="python_book.jpg"
    ),
    2: Product(
        id=2,
        name="SmartBooks: Web Development",
        description="Learn web development from scratch with HTML, CSS, and JavaScript.",
        base_price=24.99,
        image="webdev_book.jpg"
    )
}

def get_product(product_id):
    return products_db.get(int(product_id))

def get_all_products():
    return list(products_db.values())