"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import get_hash, check_password_hash

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def create_user():
    try:
        email = request.json.get("email")
        password = request.json.get("password")

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400
    
        secure_password = get_hash(password)
    
        new_user = User(email=email, password=secure_password, is_active=True)
        db.session.add(new_user)
        db.session.commit()
        # new_user.email = email
        # new_user.password = secure_password
        # new_user.is_active = True
        # db.session.add(new_user)
        # db.session.commit()
        return jsonify({"msg": "User created succesfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/login', methods=['POST'])
def login_user():

    try:
  
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400
    
        found_user = User.query.filter_by(email=email).first()

        # if found_user is None:
        # return "email or password is incorrect, please try again", 400
        if not found_user or not check_password_hash(found_user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401
    
        token = create_access_token(identity=email)
        return jsonify({"token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@api.route("/private", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@api.route("/get-hash", methods=["POST"])
def handle_get_hash():
    # to_hash = request.json.get("string")
    # return get_hash(to_hash)
    try:
        to_hash = request.json.get("string")
        hashed_string = get_hash(to_hash)
        return jsonify({"hashed_string": hashed_string}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500