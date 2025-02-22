"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Characters,Planets,Favorite_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
# ruta usuarios

@app.route('/user', methods=['GET'])
def get_all_users():
    
    data = db.session.scalars(db.select(User)).all()
    result = list(map(lambda item: item.serialize(),data))

    if result == []:
        return jsonify({"msg":"user does not exists"}), 404

    response_body = {
       "results": result  
    }

    return jsonify(response_body), 200

# ruta usuario unico
@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
    
        return jsonify({"result":user.serialize()}), 200
    except:
        return jsonify({"msg":"user do not exist"}), 404
    

# ruta characters
@app.route('/characters', methods=['GET'])
def get_all_characters():
    
    data = db.session.scalars(db.select(Characters)).all()
    result = list(map(lambda item: item.serialize(),data))

    if result == []:
        return jsonify({"msg":"user does not exists"}), 404

    response_body = {
        "results": result
    }

    return jsonify(response_body), 200

# ruta characters unico
@app.route('/characters/<int:id>', methods=['GET'])
def get_one_characters(id):
    try:
        characters = db.session.execute(db.select(Characters).filter_by(id=id)).scalar_one()
    
        return jsonify({"result":characters.serialize()}), 200
    except:
        return jsonify({"msg":"user do not exist"}), 404

# ruta planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    
    data = db.session.scalars(db.select(Planets)).all()
    result = list(map(lambda item: item.serialize(),data))

    if result == []:
        return jsonify({"msg":"user does not exists"}), 404

    # response_body = {
    #    "results": result  
    # }

    return jsonify(response_body), 200

# ruta planeta unico
@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planets(id):
    try:
        planets = db.session.execute(db.select(Planets).filter_by(id=id)).scalar_one()
    
        return jsonify({"result":planets.serialize()}), 200
    except:
        return jsonify({"msg":"user do not exist"}), 404

# post user.
@app.route('/user/', methods=['POST'])
def create_user():
    try:
        request_body=request.json
        user = db.session.execute(db.select(User).filter_by(email=request_body["email"])).scalar_one()

        return jsonify({"msg":"user exist"}), 400
    except:
        user = User(email=request_body["email"], password=request_body["password"],is_active=request_body["is_active"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg":"created"}), 201

#post planets/favs.
# 

@app.route('/favsplanets/<int:id>', methods=['POST'])
def post_fav_planet(id):
    body_data = request.json
    # print(body_data)
    # print(body_data["planet_id"])
     print(id)
    try:
        favs_planets = db.session.execute(db.select(Favorite_planets).filter_by(users_id=body_data["user_id"]).filter_by(planets_id=body_data["planet_id"])).scalar_one()
        return jsonify({"result":"ok"}), 400
    except:
        favs_planets = Favorite_planets(users_id=body_data["user_id"], planets_id=body_data["planet_id"])
        db.session.add(favs_planets)
        db.session.commit()
        #print(favs_planets.serialize())
        response_body = {
            "favs_planets": favs_planets.serialize()
        }
        return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
