from flask import Flask
from flask import request,jsonify
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
 # Import the current_user object

from flask import current_app as app
from application.models import product,category,purchased,user,Request,Cart,Request,storemanagerrequest
from .database import db
from flask import redirect, url_for
from flask import flash
from sqlalchemy.orm import query
from datetime import datetime
from flask_cors import CORS
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity,unset_jwt_cookies
from werkzeug.security import generate_password_hash, check_password_hash
from flask_caching import Cache
import redis
import json
from .business import *



from flask import request, jsonify



from flask import request, jsonify
jwt=JWTManager(app)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})
@app.route('/createproduct', methods=['POST'])
@jwt_required()

def createproduct():
    if request.method == 'POST' :
        data = request.json
        
        productname = data['productname']
        rateperunit = data['rateperunit']
        manufacturingdate = data['manufacturingdate']
        expirydate = data['expirydate']
        maxquantity = data['maxquantity']
        categoryid = data['categoryid']
        
        
        new_product = product(
            productname=productname,
            rateperunit=rateperunit,
            manufacturingdate=manufacturingdate,
            expirydate=expirydate,
            maxquantity=maxquantity,
            
        )
        print(new_product.categories)

        # for categoryid in categories:
        Category = category.query.get(categoryid)
            # if Category:
        Category.products.append(new_product)
            
        db.session.commit()
            
        return jsonify({"message": "Product created successfully"}), 201
    categories = category.query.all()


    return jsonify({"error": "Invalid request method"},categories=categories), 400



@app.route('/storemanagerlogin/request', methods=['POST'])
@jwt_required()
def req():
    if request.method == 'POST' :
        current_user_id = get_jwt_identity()
        data = request.json
        
        option = data['option']
        categor = data['categor']
        modification = data['modification']
       
        
        
        new_request = Request(
            
            option=option,
            categor=categor,
            modification=modification,
            storemanagerid=current_user_id,
            
            
        )
        
        db.session.add(new_request)         
        db.session.commit()
            
        return jsonify({"message": "Request sent successfully"}), 201


    return jsonify({"error": "Invalid request"}), 400

@app.route('/storemanagerrequests', methods=['GET'])
@jwt_required()

def get_store_manager_requests():
    try:
        # Fetch store manager requests from the database
        requests = Request.query.all()  # Assuming you have a Request model

        # Create a list to store the request data
        request_list = []
        for request in requests:
            request_data = {
                'id': request.id,
                'option': request.option,
                'categor': request.categor,
                'modification': request.modification,
                'storemanagerid': request.storemanagerid,
            }
            request_list.append(request_data)

        return jsonify({"requests": request_list}), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch requests", "details": str(e)}), 500
    
@app.route('/newsrequest', methods=['GET'])
@jwt_required()

def getsn():
    try:
        reqs = storemanagerrequest.query.all()  # Assuming you have a Request model

        # Create a list to store the request data
        request_lis = []
        for req in reqs:
            req_data = {
                'id': req.id,
                'name': req.name,
                'password': req.password,
                'email': req.email,
                'approved':req.approved
            }
            request_lis.append(req_data)

        return jsonify({"requests": request_lis}), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch requests", "details": str(e)}), 500


@app.route('/purchase/<string:productname>', methods=['POST'])
@jwt_required()

def book_product(productname):
    if request.method == 'POST':
        current_user_id = get_jwt_identity()
        
        Pro = product.query.filter_by(productname=productname).first()
        Cap = int(Pro.maxquantity)

        quantity = int(json.loads(request.form['quantity']))
        
        if quantity > Cap:
            return jsonify({'message': 'Out of stock'}), 201  

        else:
            purchase = purchased(productname=productname, quantity=quantity,userid=current_user_id)
            Pro.maxquantity=int(Pro.maxquantity)-quantity
            db.session.add(purchase)
            db.session.commit()
            rpu=Pro.rateperunit
            return jsonify({'rateperunit': rpu}), 200  

    return jsonify({'message': 'Invalid request'}), 400 


@app.route('/addtocart/<string:productname>', methods=['POST'])
@jwt_required()
def addtocart(productname):
    if request.method == 'POST':
        current_user_id = get_jwt_identity()


        quantity = json.loads(request.form['quantity'])
        
        
        car = Cart(productname=productname, quantity=quantity,userid=current_user_id)
        db.session.add(car)
        db.session.commit()
            
        return jsonify({'message': 'Your product is successfully added to cart'}), 200

    return jsonify({'message': 'Invalid request'}), 400


@app.route('/editproduct/<string:productname>', methods=['GET', 'POST'])
@jwt_required()

def editproduct(productname):
    if request.method == 'POST':
        name= product.query.filter_by(productname=productname).first()
        
        newvname=json.loads(request.form['data'])
        
        #venue=venue.query.filter_by(venue).first()
        
        name.productname=newvname
        db.session.add(name)
        db.session.commit()
        return jsonify({'message': 'Product edited successfully'}),201
    else:
    
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/deleteproduct/<string:productname>', methods=['GET', 'POST'])
@jwt_required()

def deleteproduct(productname):
    if request.method == 'POST':
        product_to_delete = product.query.filter_by(productname=productname).first()
        if product_to_delete:
            db.session.delete(product_to_delete)
            db.session.commit()
            return jsonify({"message": "Product deleted successfully"})
        else:
            return jsonify({"error": "Product not found"}), 404

    return jsonify({"product": productname})



@app.route('/createcategory', methods=['POST'])
@jwt_required()
def create_category():
    

    if request.method == 'POST':
        categoryname = json.loads(request.form['data'])
        
        #response_data.headers['Access-Control-Allow-Origin'] = '*'
        new_category = category(categoryname=categoryname)
        db.session.add(new_category)
        db.session.commit()
        response_data = {'message': 'Category created successfully'}
        return jsonify(response_data), 201  

    else:
        return jsonify({'error': 'Method not allowed'}), 405


@app.route('/editcategory/<string:categoryname>', methods=['GET', 'POST'])
@jwt_required()

def editvenue(categoryname):
    if request.method == 'POST':
        name= category.query.filter_by(categoryname=categoryname).first()
        
        newvname=json.loads(request.form['data'])
        
        
        name.categoryname=newvname
        db.session.add(name)
        db.session.commit()
        return jsonify({'message': 'Category edited successfully'}),201
    else:
    
        return jsonify({'error': 'Method not allowed'}), 405

    


@app.route('/deletecategory/<string:categoryname>', methods=['GET', 'POST'])
@jwt_required()

def deletecategory(categoryname):
    if request.method == 'POST':
        category_to_delete = category.query.filter_by(categoryname=categoryname).first()
        if category_to_delete:
            db.session.delete(category_to_delete)
            db.session.commit()
            return jsonify({"message": "Category deleted successfully"})
        else:
            return jsonify({"error": "Category not found"}), 404

    return jsonify({"category": categoryname})




        


from flask import request, jsonify

@app.route('/searchresults', methods=['GET','POST'])

def searchproducts():
    if request.method == 'POST':
        data = request.json # Get JSON data from the request

        searchby = data['searchby']  # Extract 'searchby' from JSON data
        searchterm = data['searchterm']  # Extract 'searchterm' from JSON data
        
        if searchby == 'productname':
            pro = product.query.filter(product.productname.contains(searchterm)).all()
            # Convert the results to a list of dictionaries
            pro_data = [{'productname': p.productname, 'rateperunit': p.rateperunit, 'manufacturingdate':p.manufacturingdate,'expirydate':p.expirydate,'productid':p.productid} for p in pro]
            return jsonify({'products': pro_data})

        elif searchby == 'rateperunit':
            pro = product.query.filter(product.rateperunit.contains(searchterm)).all()
            pro_data = [{'productname': p.productname, 'rateperunit': p.rateperunit, 'manufacturingdate':p.manufacturingdate,'expirydate':p.expirydate,'productid':p.productid} for p in pro]
            return jsonify({'products': pro_data})
        elif searchby == 'manufacturingdate':
            pro = product.query.filter(product.manufacturingdate.contains(searchterm)).all()
            pro_data = [{'productname': p.productname, 'rateperunit': p.rateperunit, 'manufacturingdate':p.manufacturingdate,'expirydate':p.expirydate,'productid':p.productid} for p in pro]
            return jsonify({'products': pro_data})
        elif searchby == 'expirydate':
            pro = product.query.filter(product.expirydate.contains(searchterm)).all()
            pro_data = [{'productname': p.productname, 'rateperunit': p.rateperunit, 'manufacturingdate':p.manufacturingdate,'expirydate':p.expirydate,'productid':p.productid} for p in pro]
            return jsonify({'products': pro_data})
        
        


        elif searchby == 'categoryname':
            Category = category.query.filter(category.categoryname.contains(searchterm)).first()
        
        
            products = Category.products
            
            product_data = [{'productname': p.productname,'rateperunit': p.rateperunit, 'manufacturingdate':p.manufacturingdate,'expirydate':p.expirydate,'productid':p.productid} for p in products]
            return jsonify({'products': product_data})

    return jsonify({})  # Return an empty JSON response if no data is found
from flask_security.utils import hash_password


@app.route('/signup', methods=['GET','POST'])
def userlogin():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    useremail=data.get('useremail')
    if user.query.filter_by(username=username).first():
        return jsonify({'message':'User already exists'}),400
    use=user(username=username,password=generate_password_hash(password),useremail=useremail,active=True,role='user')
    db.session.add(use)
    db.session.commit()
    return jsonify({'message':'User registered successfully'}), 201
from datetime import timedelta
@app.route('/login', methods=['GET','POST'])
def login():
    data=request.get_json() 
    username=data.get('username')
    password=data.get('password')
    use=user.query.filter_by(username=username).first()
    if not use or not check_password_hash(use.password,password):
        return jsonify({'message':'INvalid crediantials'}), 401
    access_token=create_access_token(identity=use.userid,expires_delta=timedelta(days=1))
    info_user={
        'userid':use.userid,
        'username':use.username,
        'role':use.role
    },
    return jsonify({'access_token':access_token,'user':info_user}),200
   






    



@app.route('/adminlogin', methods=['GET','POST'])

def adminlogin():
    pro = product.query.all()
    cat = category.query.all()
    
        
        
    cat_data = [{'categoryname': c.categoryname} for c in cat]
    pro_data = [{'productname': p.productname} for p in pro]
        
    response_data = {
        'message': 'Admin login successful',
        'categories': cat_data,
        'products': pro_data
    }
        
    return jsonify(response_data), 200


@app.route('/admindashboard', methods=['GET'])
@jwt_required()
def get_admindashboard_data():
    
    products = product.query.all()
    product_list = [{'productid': p.productid, 'productname': p.productname} for p in products]
    
    categories = category.query.all()
    category_list = [{'categoryid': c.categoryid, 'categoryname': c.categoryname} for c in categories]
    
    return jsonify({'products': product_list, 'categories': category_list})

@app.route('/cartitems', methods=['GET', 'POST'])
@jwt_required()
def cartdashboard():
    current_user_id = get_jwt_identity()
    car= Cart.query.filter_by(userid=current_user_id).all()
    cart_items_list = []
    for item in car:
        cart_items_list.append({
            'productname': item.productname,
            'quantity': item.quantity
        })
    
    return jsonify(cartitems=cart_items_list)

from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/userdashboard', methods=['GET', 'POST'])
@jwt_required()
def userdashboard():
    current_user_id = get_jwt_identity()  
    purchased_items = purchased.query.filter_by(userid=current_user_id).all()

    purchased_items_list = []

    for item in purchased_items:
        purchased_items_list.append({
            'productname': item.productname,
            'quantity': item.quantity
        })

    return jsonify(purchaseditems=purchased_items_list), 200




@app.route('/listcategories', methods=['GET'])

def list_category():
    categor = category.query.all()
    category_list = [{'categoryname': cat.categoryname,'categoryid': cat.categoryid } for cat in categor]
    return jsonify(categories=category_list)

@app.route('/listproducts', methods=['GET'])
@cache.cached(timeout=2)


def list_products():
    # products = product.query.all()
    products = product.query.order_by(desc(product.timeadded)).all()
    product_list = [{'productname': pro.productname,'rateperunit': pro.rateperunit,'productid':pro.productid} for pro in products]
    return jsonify(products=product_list)


@app.route('/createcategoryrequest', methods=['POST'])
def create_category_request():
    
    new_request = Request(status="pending")
    
    db.session.add(new_request)
    db.session.commit()
    
    flash('Category request submitted successfully', 'success')
    return redirect(url_for('storemanagerlogin'))


@app.route('/rejectrequest/<int:id>', methods=['POST'])


def deleter(id):
    if request.method == 'POST':
        r_to_delete = Request.query.filter_by(id=id).first()
        if r_to_delete:
            db.session.delete(r_to_delete)
            db.session.commit()
            return jsonify({"message": "Request deleted successfully"})
        else:
            return jsonify({"error": "Request not found"}), 404

    return jsonify({"requestid": id})

@app.route('/approverequest/<int:requestid>', methods=['POST'])
def approve_request(requestid):
    if request.method == 'POST':
        r_to_approve = Request.query.filter_by(id=requestid).first()
        if r_to_approve:
            if r_to_approve.option in ['edit', 'delete','create']:
                if r_to_approve.option=='create':
                    new_category = category(categoryname=r_to_approve.categor)
                    db.session.add(new_category)
                
                elif r_to_approve.option == 'edit':
                    
                    category_to_edit = category.query.filter_by(categoryname=r_to_approve.categor).first()
                    if category_to_edit:
                        category_to_edit.categoryname = r_to_approve.modification
                        db.session.add(category_to_edit)

                else:
                    
                    category_to_delete = category.query.filter_by(categoryname=r_to_approve.categor).first()
                    if category_to_delete:
                        db.session.delete(category_to_delete)

            r_to_approve.approved = True
            db.session.delete(r_to_approve)
            db.session.commit()

            return jsonify({"message": "Request approved successfully"}), 200
        else:
            return jsonify({"error": "Request not found"}), 404

    return jsonify({"requestid": requestid}), 400

@app.route('/newstoremanager', methods=['POST'])
def create_store_manager_request():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')

    requ = storemanagerrequest(name=name, password=generate_password_hash(password), email=email)
    db.session.add(requ)
    db.session.commit()

    return jsonify({'message': 'Store manager request created successfully'}), 201


@app.route('/re/<int:id>', methods=['POST'])
def er(id):
    if request.method == 'POST':
        r_to_delete = storemanagerrequest.query.filter_by(id=id).first()
        if r_to_delete:
            db.session.delete(r_to_delete)
            db.session.commit()
            return jsonify({"message": "Request deleted successfully"})
        else:
            return jsonify({"error": "Request not found"}), 404

    return jsonify({"requestid": id})



@app.route('/ap/<int:id>', methods=['POST'])
def appr(id):
    

    request_to_approve = storemanagerrequest.query.filter_by(id=id).first()

    if request_to_approve:
        new_user = user(
            username=request_to_approve.name,
            password=request_to_approve.password,
            useremail=request_to_approve.email,
            role='storemanager',
            active=True
        )

        try:
            db.session.add(new_user)
            db.session.delete(request_to_approve)  

            db.session.commit()

            return jsonify({'message': 'Request approved and user created'}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to create user', 'details': str(e)}), 500

    return jsonify({'error': 'Request not found'}), 404

from matplotlib import pyplot as plt
from io import BytesIO
from flask import Response
import matplotlib
matplotlib.use('Agg')

@app.route('/salesanalysis', methods=['GET'])
@jwt_required()
def sales_analysis():
    product_names = []
    quantities = []
    product_quantities = defaultdict(int)

    purchased_data = purchased.query.with_entities(purchased.productname, purchased.quantity).all()


    for product_name, quantity in purchased_data:
        product_quantities[product_name] += quantity

    product_names = list(product_quantities.keys())  # Extract product names
    quantities = list(product_quantities.values())
    plt.figure(figsize=(10, 6))
    plt.bar(product_names, quantities)
    plt.xlabel('Product Name')
    plt.ylabel('Quantity')
    plt.title('Sales Analysis')

    chart_filename = 'sales_chart.png'
    plt.savefig(chart_filename, bbox_inches='tight')
    plt.close()

    with open(chart_filename, 'rb') as chart_file:
        chart_data = chart_file.read()

    return Response(chart_data, content_type='image/png')

from collections import defaultdict

from flask import Response
from collections import defaultdict
import matplotlib.pyplot as plt


@app.route('/cartanalysis', methods=['GET'])
@jwt_required()
def cart_analysis():
    product_quantities = defaultdict(int)

    cart_data = Cart.query.with_entities(Cart.productname, Cart.quantity).all()

    for product_name, quantity in cart_data:
        product_quantities[product_name] += quantity

    product_names = list(product_quantities.keys())  # Extract product names
    quantities = list(product_quantities.values())  # Extract quantities

    plt.figure(figsize=(10, 6))
    plt.bar(product_names, quantities)
    plt.xlabel('Product Name')
    plt.ylabel('Quantity')
    plt.title('Cart Analysis')

    chart_filename = 'cart_chart.png'
    plt.savefig(chart_filename, bbox_inches='tight')
    plt.close()

    with open(chart_filename, 'rb') as chart_file:
        chart_data = chart_file.read()

    return Response(chart_data, content_type='image/png')
