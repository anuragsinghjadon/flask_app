from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS
import random
import traceback
import string
from models import (db, User, Client, Product, Utils, Category,Purchase)

os.environ["PYTHONBUFFERED"] = '0'
app = Flask(__name__)
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = "6d071f9f2bd3c5b7b25ab4d80963caea1ec1f2e25f182143"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

@app.route('/advisor/login',methods=['POST'])
def advisor_login():
    # I am assuming there are two html containers one for advisor and other for user
    # this one for advisor
    data = request.json
    mobile = data['mobile']
	
    print("mobile --------",mobile,flush=True)
    
    if (mobile in [''," ",None]) and not (all(map(lambda char: char.isdigit(), mobile_number))):
        return jsonify({'error':"mobile number is not valid"})

    # We can add checks like if user already added etc 
    util = Utils()
    name = 'advisor'
    otp = ''.join(random.choice(string.digits) for _ in range(6)) # we will send otp after it is generated
    token = util.generate_hash(mobile_number=mobile)
    try:
        user = User("advisor",mobile,token,otp,"advisor")
        user.add_user()	
    except Exception as e:
        traceback.print_exc(file=None) 
        return jsonify({"message":"user can-not add","token":""}),401
    
    return jsonify({"messgae":"advisor added","token":token}),200
    
    

@app.route('/advisor/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    mobile = data['mobile']
    otp = data['otp']
    token_value = db.verify_otp(mobile_number, otp)
    if token_value != None:
        # we will update otp to -1 once the user verfierd with otp so that, it can't be use again
        return jsonify(message="OTP verified successfully",token=token_value)
    else:
        return jsonify(message="Invalid OTP",token_value='')


@app.route('/advisor/add_client/<string:token>', methods=['POST'])
def add_client_route(token):
    
#    all_users = User.query.all()
        
    #print("token inside advisor -------",token)
    advisor = User.token_exists(token)
    print("advisor is ------",advisor,flush=True)
    if not advisor:
        return jsonify({'message': 'Advisor not found or invalid token'}), 400

 	# If we have list of client and their phone numbers we will insert them throught iterartions
    data = request.get_json()
    client_name = data['client_name']
    client_mobile = data['client_mobile']

    client = Client(name=client_name, mobile_number=client_mobile, token=token)
    client.add_client()

    return jsonify({
        'message': 'Client added successfully'})

@app.route('/advisor/clients/<string:token>',methods=['GET'])
def get_all_clients(token):
    clients = Client.get_clients_by_token(token)
    return jsonify({"messg":"clients list","client":clients}),201
 
@app.route('/user/login',methods=['POST'])
def user_login():
    data = request.json
    mobile = data['mobile']
    name = data['name']
    
    if (mobile in [''," ",None]) and not (all(map(lambda char: char.isdigit(), mobile_number))):
        return jsonify({'error':"mobile number is not valid"})

    # We can add checks like if user already added etc 
    otp = ''.join(random.choice(string.digits) for _ in range(6)) # we will send otp after it is generated
    token = 'nothing'
    try:
        user = User(name,mobile,token,otp,"user")
        user.add_user()	
    except Exception as e:
        traceback.print_exc(file=None)  
        return jsonify({"message":"user can-not add","token":""}),401
    
    return jsonify({"message":"user added"}),200

@app.route('/advisor/purchase_product', methods=['POST'])
def purchase_product():
    data = request.get_json()
    advisor_token = data['advisor_token']
    client_id = data['client_id']
    product_id = data['product_id']

    advisor = User.token_exists(advisor_token)
    client = Client.query.get(client_id)
    product = Product.query.get(product_id)

    if advisor and client and product:
        unique_product_link = Utils.generate_unique_link(advisor_token,client_id,product_id)
        purchase = Purchase(advisor=advisor, client=client, product=product, unique_product_link=unique_product_link)
        db.session.add(purchase)
        db.session.commit()

        return jsonify({'message': 'Product purchased successfully', 'product_link': unique_product_link}), 201
    else:
        return jsonify({'message': 'Invalid data or user not found'}), 400


@app.route('/admin/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    product_name = data['product_name']
    product_description = data['product_description']
    category_name = data['category_name']

    category = Category.query.filter_by(name=category_name).first()
    if not category:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()

    product = Product(name=product_name, description=product_description, category=category)
    db.session.add(product)
    db.session.commit()

    return jsonify({
        'message': 'Product added successfully',
        'product_id': product.id,
        'product_desc': product.description,
        'product_name': product.name,
        'category_name': category.name
    }), 201



if __name__ == '__main__':
    if not os.path.exists('site.db'):
        with app.app_context():
            db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)







