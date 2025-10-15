from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from models import Product, Bill

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    product_list = Product.query.all()
    return render_template('products.html', products=product_list)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('products'))

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    products = Product.query.all()
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        product = Product.query.get(product_id)
        total = product.price * quantity
        bill = Bill(product_name=product.name, quantity=quantity, total=total)
        db.session.add(bill)
        db.session.commit()
    bills = Bill.query.all()
    return render_template('billing.html', products=products, bills=bills)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
