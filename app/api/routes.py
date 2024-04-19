from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import Wine, wine_schema, wines_schema, db, User, Visitor, visitor_schema, visitors_schema

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
    
@api.route('/wines', methods=['POST'])
@token_required
def create_wine(current_user_token):
    name = request.json['name']
    grape_variety = request.json['grape_variety']
    region = request.json['region']
    price = request.json['price']
    user_token = current_user_token.token

    wine = Wine(name, grape_variety, region, price, user_token=user_token)

    db.session.add(wine)
    db.session.commit()

    response = wine_schema.dump(wine)
    return jsonify(response)


@api.route('/wines', methods=['GET'])
@token_required
def get_wines(current_user_token):
    a_user = current_user_token.token
    wines = Wine.query.filter_by(user_token=a_user).all()
    response = wines_schema.dump(wines)
    return jsonify(response)


@api.route('/wines/<id>', methods=['GET'])
@token_required
def get_single_wine(current_user_token, id):
    wine = Wine.query.get(id)
    response = wine_schema.dump(wine)
    return jsonify(response)


@api.route('/wines/<id>', methods=['POST', 'PUT'])
@token_required
def update_wine(current_user_token, id):
    wine = Wine.query.get(id)
    wine.name = request.json['name']
    wine.grape_variety = request.json['grape_variety']
    wine.region = request.json['region']
    wine.price = request.json['price']
    wine.user_token = current_user_token.token

    db.session.commit()
    response = wine_schema.dump(wine)
    return jsonify(response)


@api.route('/wines/<id>', methods=['DELETE'])
@token_required
def delete_wine(current_user_token, id):
    wine = Wine.query.get(id)
    db.session.delete(wine)
    db.session.commit()
    response = wine_schema.dump(wine)
    return jsonify(response)
