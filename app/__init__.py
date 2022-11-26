from flask import Flask
from flask_bootstrap import Bootstrap
from app.config import Config
from app.routes.character import character_router

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Bootstrap(app)
    
    # Registrar rutas
    app.register_blueprint(character_router)

    return app