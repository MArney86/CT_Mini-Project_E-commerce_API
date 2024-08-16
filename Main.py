from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from db_login import db_password, db_user
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from marshmallow import ValidationError
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@localhost/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Customer(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(320), unique=True)
    phone = db.Column(db.String(15))
    orders = db.relationship('Order', backref='customer', cascade='all, delete-orphan')

class CustomerAccount(db.Model):
    __tablename__ = 'Customer_Accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))
    customer = db.relationship('Customer', backref='customer_account', uselist=False)

class Order(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    expected_delivery = db.Column(db.Date)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))

order_product = db.Table('Order_Product', 
    db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key=True), 
    db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key=True)
)

class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', secondary=order_product, backref=db.backref('products'))

class ProductSchema(ma.Schema):
    id = fields.Integer()
    product_name = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    
    class Meta:
        fields = ('id', 'product_name', 'price')
        ordered = True

class OrderProductSchema(ma.Schema):
    order_id = fields.Integer()
    product_id = fields.Integer()
    class Meta:
        fields = ('order_id', 'date', 'product_id')
        ordered = True

class OrderSchema(ma.Schema):
    id = fields.Integer()
    date = fields.Date()
    expected_delivery = fields.Date()
    customer_id = fields.Integer()
    products = fields.Nested(ProductSchema(), many=True)

    class Meta:
        fields = ('id', 'customer_id', 'date', 'expected_delivery', 'products')
        ordered = True

class CustomerSchema(ma.Schema):
    name = fields.String(require=True)
    email = fields.Email(required=True)
    phone = fields.String(required=True)
    orders = fields.Nested(OrderSchema(), many=True)

    class Meta:
        fields = ('id', 'name', 'email', 'phone')

class CustomerAccountSchema(ma.Schema):
    #password regex pattern for 8 character min, atleast 1 uppercase English letter, 1 lowercase English letter, 1 digit, and 1 special character
    pw_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    username = fields.String(required=True, validate=validate.Length(min=8))
    password = fields.String(required=True, validate=validate.Regexp(pw_pattern))
    customer_id = fields.Integer(required=True)
    customer = ma.Nested(CustomerSchema())

    class Meta:
        fields = ('id', 'customer', 'username', 'password', 'customer_id',)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

customeraccount_schema = CustomerAccountSchema()
customeraccounts_schema = CustomerAccountSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

orderproduct_schema = OrderProductSchema()
orderproducts_schema = OrderProductSchema(many=True)

#Default route
@app.route('/')
def home():
    return 'Welcome to the E-commerce Management System!'

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers)

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer),200

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        #Validate and deserialize input
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "New customer added successfully"}),201

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    #Verify Customer exists and get if does
    customer = Customer.query.get_or_404(id)

    #load update data from json request
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    #add updated data to row
    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']
    db.session.commit()

    return jsonify({"message": "Customer details updated successfully"}), 200

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    #Verify Customer exists and get if does
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer removed successfully"}), 200

@app.route('/customeraccounts', methods=['GET'])
def get_customer_accounts():
    customer_accounts = CustomerAccount.query.all()
    return customeraccounts_schema.jsonify(customer_accounts)

@app.route('/customeraccounts/<int:id>', methods=['GET'])
def get_customer_account(id):
    full_customer_account = CustomerAccount.query.get(id)
    return customer_schema.jsonify(full_customer_account)

@app.route('/customeraccounts', methods=['POST'])
def add_customer_account():
    try:
        #Validate and deserialize input
        customer_account_data = customeraccount_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_customer_account = CustomerAccount(username=customer_account_data['username'], password=customer_account_data['password'], customer_id=customer_account_data['customer_id'])
    db.session.add(new_customer_account)
    db.session.commit()
    return jsonify({"message": "New Customer Account added successfully"}), 201

@app.route('/customeraccounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    #Verify Customer Account exists and get if does
    customer_account = CustomerAccount.query.get_or_404(id)
    try:
        customer_account_data = customeraccount_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    customer_account.username = customer_account_data['username']
    customer_account.password = customer_account_data['password']
    customer_account.customer_id = customer_account_data['customer_id']
    db.session.commit()
    return jsonify({"message": "Customer Account updated successfully"})

@app.route('/customeraccounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    #Verify Customer exists
    customer_account = CustomerAccount.query.get_or_404(id)
    db.session.delete(customer_account)
    db.session.commit()
    return jsonify({"message": "Customer Account removed successfully"}), 200

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return order_schema.jsonify(product),200

@app.route('/products', methods=['POST'])
def add_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages),400
    new_product = Product(product_name=product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product was added successfully"}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    product.product_name = product_data['product_name']
    product.price = product_data['price']
    db.session.commit()
    return jsonify({"message": "Product updated successfully"}),200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200

@app.route('/orders', methods=['POST'])
def add_order():
    try:
        order_data = order_schema.load(request.json)
        order_params = request.args.to_dict(flat=False)
    except ValidationError as err:
        return jsonify(err.messages),400
    
    try:
        order_products = order_params['Product']

        new_order = Order(customer_id=order_data['customer_id'],date=order_data['date'],expected_delivery=order_data['expected_delivery'])
        
        for i in range(len(order_products)):
                add_product = db.session.query(Product).filter(Product.id == order_products[i]).first()
                new_order.products.append(add_product)
        db.session.add(new_order)
        db.session.commit()

    except ValidationError as err:
        return jsonify(err.messages),400

    return jsonify({"message": "Order was added successfully"}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return orders_schema.jsonify(orders)

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return order_schema.jsonify(order),200

@app.route('/orders/track_by_id', methods=['GET'])
def track_order_by_id():
    order_id = request.args.get('order_id')
    order = Order.query.filter(Order.id == order_id).first()
   
    tracking_info = {
        "Date Ordered" : order.date,
        "Expected Delivery Date" : order.expected_delivery
    }
    return jsonify(tracking_info), 200

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    order.customer_id = order_data['customer_id']
    order.date = order_data['date']
    order.expected_delivery = order_data['expected_delivery']
    db.session.commit()
    return jsonify({"message": "Order updated successfully"}),200

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully"}), 200

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

