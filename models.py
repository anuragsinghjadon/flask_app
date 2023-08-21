from flask_sqlalchemy import SQLAlchemy
import hashlib
import secrets
import string 
import traceback
import random
import string 
# db_url = "mysql://username:password@hostname:port/database_name"

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    otp = db.Column(db.String(5), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    token = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(200),nullable=True)
    
    def __init__(self, name,mobile_number,token, otp, role):
        self.name = name
        self.mobile_number = mobile_number
        self.token = token
        self.otp = otp
        self.role = role
        
    def add_user(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            traceback.print_exc(file=None)
            print("User not added")
            
    @classmethod
    def token_exists(cls, token):
        print("cls is --------",cls)
        #print(cls.query.filter_by(token="63d02295"),flush=True)
        return cls.query.filter_by(token=token).first() is not None
        

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    token = db.Column(db.String(8), nullable=True)
    
    def __init__(self, name,mobile_number, token):
        self.name = name
        self.mobile_number = mobile_number
        self.token = token
    
    def add_client(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            traceback.print_exc(file=None)
            print("client didn't added")
            
    @classmethod
    def get_clients_by_token(cls, token):
        clients = cls.query.filter_by(token=token).all()
        
        client_details = [{'id': client.id, 'name': client.name} for client in clients]
        return client_details

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    unique_product_link = db.Column(db.String(100), nullable=False)
    
    advisor = db.relationship('User', foreign_keys=[advisor_id])
    client = db.relationship('Client', foreign_keys=[client_id])
    product = db.relationship('Product', foreign_keys=[product_id])

class Utils():

    def generate_hash(self,mobile_number,length=8):
        if mobile_number not in [''," ",None]:
            print("insdie hash generation --------")
            symbols = string.ascii_letters + string.digits + string.punctuation + str(mobile_number)
            random_symbols = ''.join(secrets.choice(symbols) for _ in range(length))
            hash_object = hashlib.sha256(random_symbols.encode())
            hash_hex = hash_object.hexdigest()
            print("----------",hash_hex[:length])
            return hash_hex[:length]
        else:
            print("We can not generate token as mobile number is not valid")
            return ''
    
    def generate_unique_link(advisor_token, client_id, product_id):
        unique_string = f"{advisor_token}-{client_id}-{product_id}"
        md5_hash = hashlib.md5(unique_string.encode()).hexdigest()
        unique_link = f"https://abc.com/purchase/{md5_hash}"
        return unique_link

