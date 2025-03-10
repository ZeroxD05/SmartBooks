from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
import json
from config import Config
from models.product import get_product, get_all_products
from models.cart import Cart
from models.order import Order, save_order

app = Flask(__name__)
app.config.from_object(Config)
Session(app)

# Initialize cart in session if not present
@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = {'items': []}


# Routes
@app.route('/')
def index():
    products = get_all_products()
    return render_template('index.html', products=products)


@app.route('/products')
def products():
    products = get_all_products()
    return render_template('products.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('products'))
    return render_template('product.html', product=product)


@app.route('/cart')
def cart():
    cart_data = session.get('cart', {'items': []})
    cart_items = []
    total_price = 0
    
    for i, item in enumerate(cart_data['items']):
        product = get_product(item['product_id'])
        if product:
            price = product.get_price_for_size(item['size']) * item['quantity']
            cart_items.append({
                'index': i,
                'product': product,
                'size': item['size'],
                'color': item['color'],
                'quantity': item['quantity'],
                'price': price
            })
            total_price += price
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    size = request.form.get('size')
    color = request.form.get('color')
    quantity = int(request.form.get('quantity', 1))
    
    product = get_product(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('products'))
    
    cart_data = session.get('cart', {'items': []})
    
    # Check if the item already exists in the cart
    for item in cart_data['items']:
        if (item['product_id'] == int(product_id) and 
            item['size'] == size and 
            item['color'] == color):
            item['quantity'] += quantity
            session['cart'] = cart_data
            flash('Item quantity updated in cart', 'success')
            return redirect(url_for('cart'))
    
    # If not, add a new item
    cart_data['items'].append({
        'product_id': int(product_id),
        'size': size,
        'color': color,
        'quantity': quantity
    })
    
    session['cart'] = cart_data
    flash('Item added to cart', 'success')
    return redirect(url_for('cart'))


@app.route('/update_cart', methods=['POST'])
def update_cart():
    action = request.form.get('action')
    index = int(request.form.get('index'))
    
    cart_data = session.get('cart', {'items': []})
    
    if action == 'remove' and 0 <= index < len(cart_data['items']):
        cart_data['items'].pop(index)
        flash('Item removed from cart', 'success')
    
    elif action == 'update':
        quantity = int(request.form.get('quantity', 1))
        if 0 <= index < len(cart_data['items']):
            cart_data['items'][index]['quantity'] = max(1, quantity)
            flash('Cart updated', 'success')
    
    session['cart'] = cart_data
    return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    cart_data = session.get('cart', {'items': []})
    if not cart_data['items']:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart'))
    
    cart_items = []
    total_price = 0
    
    for item in cart_data['items']:
        product = get_product(item['product_id'])
        if product:
            price = product.get_price_for_size(item['size']) * item['quantity']
            cart_items.append({
                'product': product,
                'size': item['size'],
                'color': item['color'],
                'quantity': item['quantity'],
                'price': price
            })
            total_price += price
    
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)


@app.route('/place_order', methods=['POST'])
def place_order():
    cart_data = session.get('cart', {'items': []})
    if not cart_data['items']:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart'))
    
    # Collect customer information from form
    customer_info = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'address': request.form.get('address'),
        'city': request.form.get('city'),
        'zip': request.form.get('zip'),
        'country': request.form.get('country')
    }
    
    # Calculate total price
    total_price = 0
    cart_items = []
    
    for item in cart_data['items']:
        product = get_product(item['product_id'])
        if product:
            price = product.get_price_for_size(item['size']) * item['quantity']
            cart_items.append({
                'product_id': item['product_id'],
                'product_name': product.name,
                'size': item['size'],
                'color': item['color'],
                'quantity': item['quantity'],
                'price': price
            })
            total_price += price
    
    # Create order
    order = Order(customer_info, cart_items, total_price)
    order_id = save_order(order)
    
    # Clear cart
    session['cart'] = {'items': []}
    
    return redirect(url_for('confirmation', order_id=order_id))


@app.route('/confirmation/<order_id>')
def confirmation(order_id):
    from models.order import get_order
    order = get_order(order_id)
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('confirmation.html', order=order)


@app.route('/clear_cart')
def clear_cart():
    session['cart'] = {'items': []}
    flash('Cart cleared', 'success')
    return redirect(url_for('cart'))


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)