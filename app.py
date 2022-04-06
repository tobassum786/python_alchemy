from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db.sqlite3'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '3UPijOcTgh7oo7qBR0cDsA'

db = SQLAlchemy(app)
# db.init_app(app)

# Making Tables
class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	address = db.Column(db.String(500), nullable=False)
	city = db.Column(db.String(500), nullable=False)
	postcode = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(50), nullable=True, unique=True)

	# Relation with backrefernce to order
	orders = db.relationship('order', backref='customer')

order_product = db.Table('order_product',
	db.Column('order_id', db.Integer, ForeignKey('order.id'), primary_key=True),
	db.Column('Product_id', db.Integer, ForeignKey('product.id'), primary_key=True)
	)

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	order_date = db.Column(db.DateTime, nullable=False, defualt=datetime.utcnow())
	shipped_date = db.Column(db.DateTime)
	delivered_date = db.Column(db.DateTime)
	cupon_code = db.Column(db.String(50))

	# Make Relationships
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

	products = db.relationship('products', secondary=order_product)
   
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False, unique=True)
	price = db.Column(db.Integer, nullable=False)



@app.route('/')
def index():
	return "Hello World"

if __name__=='__main__':
	app.run(debug=True)