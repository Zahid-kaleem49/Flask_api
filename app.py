from pickle import TRUE
from urllib import response
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import json



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)






class Vendor(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    cartitems = db.relationship(
        'Cartitem', backref='vendor', cascade="all, delete")
    
    
    
    
    

class Cartitem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), nullable=False)
    product_price = db.Column(db.Float(10), nullable=False)
    product_quantity = db.Column(db.Float(100), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)


    def __repr__(self):
        return '<Cart %r>' % self.product_name



@app.route("/")
def helloworld():
    return "Hello World!"


@app.route('/new/', methods=['POST'])
def newitem():
    # request_data = request.get_json()
     data = request.json
     name = data['vendor_name']
     email = data['email']
     ven = Vendor(vendor_name=name, email= email)
     db.session.add(ven)
     db.session.commit()
     
     pname = data['product_name']
     pprice = data['product_price']
     pquantity = data['product_quantity']
     if ven:
        cart = Cartitem(vendor_id=ven.id,product_name = pname, product_price=pprice, product_quantity= pquantity)
        db.session.add(cart)
        db.session.commit()
        return jsonify({"status": "success"}), 200
     
 
@app.route('/update/<int:id_>/', methods=['PUT'])
def updateitem(id_):
    data = request.json
    vendor = Vendor.query.filter_by(id=id_).first()
    cart = vendor.cartitems
    print(cart)
    if cart and data:
        cart[0].product_name = data['product_name']
        cart[0].product_price = data['product_price']
        cart[0].product_quantity = data['product_quantity']
        print("here")
        db.session.commit()
        # print(cart)
        return jsonify({"status": "success"}), 200
    
@app.route('/delete/<int:id_>', methods=['DELETE'])
def deleteietm(id_):
    if vendor := Vendor.query.filter_by(id=id_).first():
        print(vendor)
        db.session.delete(vendor)
        db.session.commit()
        return jsonify({"status": "success"}), 200

    return jsonify({"status": "unsuccess"}), 404
    

@app.route('/cart/<int:id_>', methods=['GET'])
def getitem(id_):
    if  vendor:= Vendor.query.filter_by(id=id_).first():
        print(vendor)
        cart_items = []
        print(vendor.cartitems)
        for cartitem in vendor.cartitems:
            data = cartitem.__dict__
            print(data)
            data.pop('_sa_instance_state', None)
            cart_items.append(data)
        vendor_details = vendor.__dict__
        print(vendor_details)
        vendor_details['cart_items'] = cart_items
        vendor_details.pop('_sa_instance_state', None)
        vendor_details.pop('cartitems', None)
        print(vendor_details)
        return jsonify({"data": vendor_details}), 200

    
       
if __name__ == "__main__":
    app.run(debug=True)
