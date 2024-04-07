from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Visitor, visitor_schema, visitors_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Good': 'job'}

@api.route('/visitors', methods = ['POST'])
@token_required
def create_visitor(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    visitor = Visitor(name, email, phone_number, address, user_token = user_token )

    db.session.add(visitor)
    db.session.commit()

    response = visitor_schema.dump(visitor)
    return jsonify(response)

@api.route('/visitors', methods = ['GET'])
@token_required
def get_visitor(current_user_token):
    a_user = current_user_token.token
    visitors = Visitor.query.filter_by(user_token = a_user).all()
    response = visitors_schema.dump(visitors)
    return jsonify(response)


@api.route('/visitors/<id>', methods = ['GET'])
@token_required
def get_single_visitor(current_user_token, id):
    visitor = Visitor.query.get(id)
    response = visitor_schema.dump(visitor)
    return jsonify(response)


#Update endpoint
@api.route('/visitors/<id>', methods = ['POST','PUT'])
@token_required
def update_visitor(current_user_token,id):
    visitor = Visitor.query.get(id) 
    visitor.name = request.json['name']
    visitor.email = request.json['email']
    visitor.phone_number = request.json['phone_number']
    visitor.address = request.json['address']
    visitor.user_token = current_user_token.token

    db.session.commit()
    response = visitor_schema.dump(visitor)
    return jsonify(response)

# Delete Endpoint
@api.route('/visitors/<id>', methods = ['DELETE'])
@token_required
def delete_visitor(current_user_token, id):
    visitor = Visitor.query.get(id)
    db.session.delete(visitor)
    db.session.commit()
    response = visitor_schema.dump(visitor)
    return jsonify(response)
    

    