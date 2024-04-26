from app import data_base


def cart_contents(session):
    db = data_base.DATABASE()
    products = []
    to_pay = 0
    index = 0
    for item in session:
        product = db.select_product_from_id(id=item['id'])
        total = item['quantity'] * product[1].price
        to_pay += total
        index += 1
        products.append(
            {'id': product[1].id, 'name': product[1].product_name, 'price': product[1].price,
             'quantity': item['quantity'], 'total': total, 'index': index,
             'category_name': product[0].category_name})
    product_to_cart = len(products)
    return products, to_pay, product_to_cart


def add_product_to_cart(session, id: int, quantity: int = 1):
    dict_keys = []
    for x in session:
        dict_keys.append(int(x['id']))
    if int(id) in dict_keys:
        for x in session:
            if int(id) == x['id']:
                x['quantity'] += 1
    else:
        session.append({'id': int(id), 'quantity': quantity})
