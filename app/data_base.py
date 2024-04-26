from app import app
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    products = db.relationship('Product', backref='category')

    def __init__(self, category_name):
        self.category_name = category_name


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    specification = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __init__(self, product_name, category, price, specification, quantity):
        self.product_name = product_name
        self.category_id = category
        self.price = price
        self.specification = specification
        self.quantity = quantity


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firs_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Integer, default=datetime.utcnow(), nullable=False)
    order_details = db.relationship('OrderDetails', backref='order')

    def __init__(self, first_name, last_name, city, number, date):
        self.firs_name = first_name
        self.last_name = last_name
        self.city = city
        self.number = number
        self.date = date


class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    def __init__(self, product_id, product_name, price, quantity, order_id):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.order_id = order_id


class DATABASE:
    def add_category(self, category_name: str):
        all_categories_from_db = Category.query.all()
        all_categories = ()
        for category in all_categories_from_db:
            all_categories += (category.category_name,)
        if category_name not in all_categories:
            category = Category(category_name)
            db.session.add(category)
            db.session.commit()
        category_id = Category.query.filter_by(category_name=category_name).first().id
        return category_id

    def add_product(self, product_name: str, category: int, price: int, specification: str, quantity: int = 1):
        all_product_name_from_db = Product.query.all()
        all_product_name = ()
        for name in all_product_name_from_db:
            all_product_name += (name.product_name,)
        if product_name in all_product_name:
            Product.query.filter(Product.product_name == product_name). \
                update({Product.quantity: Product.quantity + quantity})
            db.session.commit()
        else:
            product = Product(product_name, category, price, specification, quantity)
            db.session.add(product)
            db.session.commit()

    def add_product_from_json(self, json_file):
        product_json = json.load(open(json_file, encoding='utf-8'))
        for category_name in product_json:
            category = self.add_category(category_name=category_name)
            for product in product_json[category_name]:
                self.add_product(product_name=product, category=category, price=product_json[category_name][product][0],
                                 specification=product_json[category_name][product][1])

    def add_order(self, first_name, last_name, city, telephone, date):
        order = Order(first_name, last_name, city, telephone, date)
        db.session.add(order)
        db.session.commit()

    def add_order_details(self, product_id, product_name, price, quantity, order_id):
        order_details = OrderDetails(product_id, product_name, price, quantity, order_id)
        db.session.add(order_details)
        db.session.commit()

    def select_product_from_id(self, id: int):
        product = db.session.query(Category, Product).\
            outerjoin(Product, Category.id == Product.category_id).filter(Product.id == id).first()
        return product

    def select_product(self, id: int):
        product = db.session.query(Category, Product).outerjoin(
            Product, Category.id == Product.category_id).filter(Product.id == id).first()
        return product

    def select_last_order(self):
        last_order = Order.query.order_by(Order.id.desc()).first().id
        return last_order

    def select_all_categories(self):
        all_categories_form_db = Category.query.all()
        return all_categories_form_db

    def select_products_from_category(self, category_id: int, page_num: int = 1):
        all_products_in_category = db.session.query(Category, Product).\
            outerjoin(Product, Category.id == Product.category_id).filter(Category.id == category_id).\
            paginate(per_page=6, page=page_num, error_out=False)
        return all_products_in_category
