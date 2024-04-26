from app import app
from app import data_base
from app import forms
from app import datas
import flask
from datetime import datetime


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'cart' not in flask.session:
        flask.session['cart'] = []
    cart_contents = datas.cart_contents(flask.session['cart'])
    db = data_base.DATABASE()
    categories = db.select_all_categories()
    return flask.render_template('index.html', cart_products=cart_contents[0], to_pay=cart_contents[1],
                                 quantity_in_cart=cart_contents[2], categories=categories)


@app.route('/category/<int:category_id>', methods=['GET', 'POST'])
@app.route('/category/<int:category_id>/<int:page_num>', methods=['GET', 'POST'])
def products_from_category(category_id, page_num=1):
    db = data_base.DATABASE()
    products = db.select_products_from_category(category_id=category_id, page_num=page_num)
    form = forms.AddCart()
    cart_contents = datas.cart_contents(flask.session['cart'])
    return flask.render_template('products.html', products=products, form=form,
                                 cart_products=cart_contents[0], to_pay=cart_contents[1],
                                 quantity_in_cart=cart_contents[2])


@app.route('/product/<id>', methods=['GET', 'POST'])
def product(id):
    db = data_base.DATABASE()
    product_card = db.select_product(id=id)
    specification = product_card[1].specification.split(";")
    form = forms.AddCart()
    cart_contents = datas.cart_contents(flask.session['cart'])
    return flask.render_template('product.html', product_card=product_card, specification=specification, form=form,
                                 cart_products=cart_contents[0], to_pay=cart_contents[1],
                                 quantity_in_cart=cart_contents[2])


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = forms.AddCart()
    if form.validate_on_submit():
        datas.add_product_to_cart(flask.session['cart'], form.id.data, form.quantity.data)
        flask.session.modified = True
    cart_contents = datas.cart_contents(flask.session['cart'])
    return flask.render_template('cart.html', cart_products=cart_contents[0], to_pay=cart_contents[1],
                                 quantity_in_cart=cart_contents[2])


@app.route('/quick-add-to-cart/<id>')
def quick_add_to_cart(id):
    if 'cart' not in flask.session:
        flask.session['cart'] = []
    datas.add_product_to_cart(flask.session['cart'], id)
    flask.session.modified = True
    return flask.redirect(flask.url_for('cart'))


@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del flask.session['cart'][int(index) - 1]
    flask.session.modified = True
    return flask.redirect(flask.url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = forms.Checkout()
    cart_contents = datas.cart_contents(flask.session['cart'])
    return flask.render_template('checkout.html', form=form, cart_products=cart_contents[0], to_pay=cart_contents[1],
                                 quantity_in_cart=cart_contents[2])


@app.route('/success', methods=['GET', 'POST'])
def success():
    db = data_base.DATABASE()
    form = forms.Checkout()
    last_order_id = None
    now = datetime.now().strftime("%d.%m.%y")
    cart_contents = datas.cart_contents(flask.session['cart'])
    if form.validate_on_submit():
        db.add_order(form.first_name.data, form.last_name.data, form.city.data, form.telephone.data, now)
        last_order_id = db.select_last_order()
        for product in cart_contents[0]:
            db.add_order_details(product['id'], product['name'], product['price'],
                                 product['quantity'], order_id=last_order_id)
        del flask.session['cart']
        flask.session.modified = True
    return flask.render_template('success.html', form=form, now=now, cart_products=cart_contents[0],
                                 to_pay=cart_contents[1], quantity_in_cart=cart_contents[2], order_id=last_order_id)


@app.route('/about', methods=['GET', 'POST'])
def about():
    cart_contents = datas.cart_contents(flask.session['cart'])
    return flask.render_template('about.html', cart_products=cart_contents[0], to_pay=cart_contents[1],
                                 quantity_in_cart=cart_contents[2])


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    cart_contents = datas.cart_contents(flask.session['cart'])
    return flask.render_template('contacts.html', cart_products=cart_contents[0], to_pay=cart_contents[1],
                                 quantity_in_cart=cart_contents[2])
