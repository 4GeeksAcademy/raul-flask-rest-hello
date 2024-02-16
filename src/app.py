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
from models import db, User, People, Planet, Favorite
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

################################################################################################
#######################---GET---################################################################
# EJERCICIO
@app.route('/favorite', methods=['GET'])
def get_favorite():
    # ID del usuario
    user_id = 1 
    # Para mostrar los favoritos de un usuario en concreto, filtro los favoritos por el id del usuario
    favorites = Favorite.query.filter_by(user_id=user_id).all()

    result = [favorite.serialize() for favorite in favorites]

    return jsonify(result)

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()

    result = []

    for people in all_people:
        result.append(people.serialize())
    
    return jsonify(result), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    all_planet = Planet.query.all()

    result = []

    for planet in all_planet:
        result.append(planet.serialize())
    
    return jsonify(result), 200

###########################---GET-INDIVIDUAL-ID---#############################

@app.route('/favorite/people/<int:people_id>', methods=['GET'])
def get_id_person(people_id):
    people = People.query.get(people_id)
    if people is None:
        raise APIException("El personaje no existe", status_code=404)
    return jsonify(people.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['GET'])
def get_id_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("El planeta no existe", status_code=404)
    return jsonify(planet.serialize()), 200

###########################---POST---#####################################

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    # Id de usuario
    user_id = 1
    # Creación del favorito según del id
    favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Personaje añadido"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # Id de usuario
    user_id = 1
    # Creación del favorito según del id
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Planeta añadido"}), 201


###########################################################################################
###########################################################################################

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
