from .database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_security import UserMixin , RoleMixin 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf import FlaskForm

import uuid
class user(db.Model, UserMixin):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(258), unique=True, nullable=True)
    password = db.Column(db.String(272), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    useremail = db.Column(db.String(269))
    active = db.Column(db.Boolean())
    role =db.Column(db.String(255))
   



productcategoryassociation = db.Table(
    'productcategoryassociation',
    db.Column('productid', db.Integer, db.ForeignKey('product.productid')),
    db.Column('categoryid', db.Integer, db.ForeignKey('category.categoryid'))
)

class category(db.Model):
    __tablename__ = 'category'
    categoryid = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(50), nullable=False)
    products = db.relationship(
        'product',
        secondary=productcategoryassociation,
        back_populates='categories'
    )
       

class product(db.Model):
    __tablename__ = 'product'
    productid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(50), nullable=False)


    manufacturingdate = db.Column(db.String(100), nullable=False)
    expirydate = db.Column(db.String(100), nullable=False)
    rateperunit = db.Column(db.Float, nullable=False)
    maxquantity = db.Column(db.String(100), nullable=False)
    timeadded = db.Column(db.DateTime, default=datetime.utcnow)
    categories = db.relationship(
        'category',
        secondary=productcategoryassociation,
        back_populates='products'
    )




class purchased(db.Model):
    __tablename__ = 'purchased'
    purchasingid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    productname = db.Column(db.String(50), db.ForeignKey('product.productname'), nullable=False)
    quantity= db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(250))
    modification= db.Column(db.String(250))
    categor=db.Column(db.String(250))
    storemanagerid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)

    productname = db.Column(db.String(50), db.ForeignKey('product.productname'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class storemanagerrequest(db.Model):
    __tablename__ = 'storemanagerrequest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    approved = db.Column(db.Boolean, default=False)