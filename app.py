from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '3UPijOcTgh7oo7qBR0cDsA'

db = SQLAlchemy(app)
# db.init_app(app)

# Making Tables
class Customer(db.Model):
	id = db.Column(db.integer, primary_key=True)
	first_name = db.Column(db.string(50), nullable=False)
	last_name = db.Column(db.string(50), nullable=False)
	address = db.Column(db.string(500), nullable=False)
	city = db.Column(db.string(500), nullable=False)
	postcode = db.Column(db.string(50), nullable=False)
	email = db.Column(db.string(50), nullable=True, unique=True)


class Order(db.Model):
	id = db.Column(db.integer, primary_key=True)
	order_date = db.Column(db.DateTime, nullable=False defualt=datetime.utcnow())
	shipped_date = db.Column(db.DateTime, datetime)
	delivered_date = db.Column(db.DateTime, datetime)
	cupon_code = db.Column(db.string(50))



class Product(db.Model):
	id = db.Column(db.integer, primary_key=True)
	name = db.Column(db.string(50), nullable=False, unique=True)
	price = db.Column(db.integer, nullable=False)



@app.route('/')
def index():
	return "Hello World"

if __name__=='__main__':
	app.run(debug=True)