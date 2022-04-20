from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

import random

from datetime import datetime

fake = Faker()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '3UPijOcTgh7oo7qBR0cDsA'

db = SQLAlchemy(app)
# db.init_app(app)

# Making Tables
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column (db.String(50), nullable=False)
    last_name = db.Column (db.String(50), nullable=False) 
    address = db.Column (db.String(500), nullable=False)
    city = db.Column (db.String(50), nullable=False)
    postcode = db.Column (db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    orders = db.relationship('Order', backref='customer')

order_product = db.Table('order_product',
	db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
	db.Column('Product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
	)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column (db.DateTime, nullable=False, default=datetime.utcnow)
    shipped_date = db.Column(db. DateTime)
    delivered_date = db.Column(db.DateTime)
    coupon_code = db.Column(db.String (50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
   
    products = db.relationship('Product', secondary=order_product)
   
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False, unique=True)
	price = db.Column(db.Integer, nullable=False)



# Make Fake database with Customers, Products and Orders

def add_customers():
	for _ in range(100):
		customer = Customer(
			first_name = fake.first_name(),
			last_name = fake.last_name(),
			address = fake.street_address(),
			city = fake.city(),
			postcode = fake.postcode(),
			email = fake.email(),
			)
		db.session.add(customer)
	db.session.commit()

# Creating Fake Orders


def add_orders():
	customers = Customer.query.all()

	for _ in range(1000):
		# find a random customer
		customer = random.choice(customers)

		ordered_date = fake.date_time_this_year()
		shipped_date = random.choices([None, fake.date_time_between(start_date=ordered_date)], [10, 90])[0]

		delivered_date = None
		if shipped_date:
			delivered_date = random.choices([None, fake.date_time_between(start_date=shipped_date)], [50, 500])[0]

		coupon_code =random.choices([None, '50OFF', 'FREESHIPPING', 'BYEONEGETONE'],[80, 5, 5, 5])[0]


		order = Order(
				customer_id = customer.id,
				order_date = ordered_date,
				shipped_date = shipped_date,
				delivered_date = delivered_date,
				coupon_code = coupon_code
			)
		db.session.add(order)
	db.session.commit()

# Create Products like a colors name

def add_products():
	for _ in range(10):

		product = Product(
				name = fake.color_name(),
				price = random.randint(10, 100)
			)
		db.session.add(product)
	db.session.commit()

# Make order with fake customer and products	

def add_order_products():
	orders = Order.query.all()
	products = Product.query.all()

	for order in orders:
		k = random.ranint(1, 3)

		purchased_products = random.sample(products, k)
		order.products.extend(purchased_products)

	db.session.commit()

# create a random orders

def create_random_data():
	db.create_all()
	add_customers()
	add_orders()
	add_products()
	add_order_products()


if __name__=='__main__':
	app.run(debug=True)