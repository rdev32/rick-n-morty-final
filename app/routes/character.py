from flask import Blueprint, render_template
from app.db import DabataseConnection
from app.models.character import Character
import requests

character_router = Blueprint('character_router', __name__)
db = DabataseConnection(5)

@character_router.route('/')
def index():
    characters = db.collection.find().sort('_id', -1)
    return render_template('index.html', characters=characters)

@character_router.route('/profile/<id>')
def profile(id):
    id = int(id)
    data = db.collection.find_one({ '_id': id })
    return render_template('profile.html', pj_data=data)

@character_router.route('/load')
def cargar():
    for n in range(db.npags):
        r = requests.get(db.url + str(n+1))
        json = r.json()
        lista_jsons = json["results"]

        for element in lista_jsons:
            first_episode = element['episode'][0]
            ep = requests.get(first_episode)
            data = ep.json()
            first_episode = data['name']
            
            character = Character(
                _id=element['id'],
                name=element['name'],
                alive=element['status'],
                species=element['species'],
                typo=element['type'],
                gender=element['gender'],
                origin=element['origin']['name'],
                location_name=element['location']['name'],
                image_url=element['image'],
                episode=first_episode,
                created=element['created'],
                episode_n=element['episode']
            )
            db.collection.insert_one(character.to_json())
    
    return 'Cargado exitosamente'