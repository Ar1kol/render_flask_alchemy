from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_data.sqlite3'
app.config['SECRET_KEY'] = "random string"
CORS(app)
db = SQLAlchemy(app)
#model

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(50))
    category = db.relationship('Product', lazy='select', backref=db.backref('category', lazy='joined'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)


    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id
    
    def __repr__(self):
        return f"{self.name} - {self.price}"
    
#model

#views
@app.route('/products/<id>')
@app.route('/products/')
def show_products(id=-1):
    if int(id) > -1:
        res = []
        for product in Product.query.filter_by(category_id = id):
            res.append({"id":product.id,"name":product.name,"price":product.price,"category":product.category_id})
        return json.dumps(res)
    else:
        res = []
        for product in Product.query.all():
            res.append({"id":product.id,"name":product.name,"price":product.price,"category":product.category_id})
        return json.dumps(res)

@app.route('/categories')
def show_categories():
    res = []
    for category in Category.query.all():
        res.append({"id":category.id,"name":category.name})
    return json.dumps(res)


@app.route('/new_category', methods = ['POST'])
def new_category():
    request_data = request.form
    name= request_data["name"]
    new_cat= Category(name)
    db.session.add (new_cat)
    db.session.commit()
    return f"category {name} added"


@app.route('/new_product', methods = ['POST'])
def new_product():
    request_data = request.form
    print(request_data)
    name= request_data["name"]
    price= request_data["price"]
    category_id = request_data["catId"]
    newProduct= Product(name, price, category_id)
    db.session.add (newProduct)
    db.session.commit()
    return f"product {name} added"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)

