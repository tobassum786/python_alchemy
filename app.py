from flask import Flask 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '3UPijOcTgh7oo7qBR0cDsA'

db = SQLAlchemy(app)
# db.init_app(app)


@app.route('/')
def index():
	return "Hello World"

if __name__=='__main__':
	app.run(debug=True)