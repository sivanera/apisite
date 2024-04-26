from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, IntegerField


class AddCart(FlaskForm):
    id = HiddenField(label='ID')
    quantity = IntegerField(label='Quantity')


class Checkout(FlaskForm):
    first_name = StringField(label='Fist_Name')
    last_name = StringField(label='Last_Name')
    city = StringField(label='City')
    telephone = StringField(label='Telephone')
