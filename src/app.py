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
from models import db, User,Characters,Planets
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

    response_body = {
       "results": result  
    }

    return jsonify(response_body), 200

# ruta planeta unico
@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planets(id):
    try:
        planets = db.session.execute(db.select(Planets).filter_by(id=id)).scalar_one()
    
        return jsonify({"result":planets.serialize()}), 200
    except:
        return jsonify({"msg":"user do not exist"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
