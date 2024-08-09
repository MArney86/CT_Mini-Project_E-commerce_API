from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from db_login import db_password, db_user
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from marshmallow import ValidationError



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@localhost/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class CustomerSchema(ma.Schema):
    name = fields.String(require=True)
    email = fields.Email(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("name", "email", "phone", "id")

class ProductSchema(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    stock_quantity = fields.Integer(required=True,validate=validate.Range(min=0))

    class Meta:
        fields = ("name", "price", "id")

class OrderSchema(ma.Schema):
    date = fields.Date(required=True)
    expected_delivery = fields.Date(required=True)
    customer_id = fields.Integer(required=True)

    class Meta:
        fields = ("date", "expected_delivery", 'customer_id', 'id')

class CustomerAccountSchema(ma.Schema):
    username = fields.String(required=True, validate=validate.Length(min=8))
    password = fields.String(required=True, validate=validate.Length(min=8,max=16))
    customer_id = fields.Integer(required=True)

    class Meta:
        fields = ('username', 'password', 'customer_id', 'id')

class OrderProductSchema(ma.Schema):
    order_id = fields.Integer(required=True)
    product_id = fields.Integer(required=True)
    order_quantity = fields.Integer(required=True, validate=validate.Range(min=0))

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

customeraccount_schema = CustomerAccountSchema()
customeraccounts_schema = CustomerAccountSchema(many=True)

orderproduct_schema = OrderProductSchema()
orderproducts_schema = OrderProductSchema(many=True)

class Customer(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(320))
    phone = db.Column(db.String(15))
    orders = db.relationship('Order', backref='customer')

class Order(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    expected_delivery = db.Column(db.Date, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))

class CustomerAccount(db.Model):
    __tablename__ = 'Customer_Accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))
    customer = db.relationship('Customer', backref='customer_account', uselist=False)

order_product = db.Table('Order_Product', 
    db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key=True), 
    db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key=True),
    db.Column('order_quantity', db.Integer, nullable=False)
)
class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', secondary=order_product, backref=db.backref('products'))

