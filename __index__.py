from pathlib import Path
from database import db
from flask import Flask
from flask_cors import CORS
from routes import routes
from models import User, Role, UserRole, JWT, Category, Product, ProductImg, Order, OrderItem
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app, supports_credentials=True)

for route in routes:
    app.register_blueprint(route, url_prefix='/api')


@app.errorhandler(404)
def not_found_error(error):
    return 'Url not found', 404


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    with db:
        db.create_tables([
            User, Role, UserRole, JWT, Category,
            Product, ProductImg, Order, OrderItem])
    app.run(debug=os.environ.get('DEBUG') or False, port=os.environ.get('PORT'))
