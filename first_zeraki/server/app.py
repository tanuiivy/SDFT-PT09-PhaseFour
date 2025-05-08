from flask import Flask
from flask_migrate import Migrate
from models.soldier import db
from views.soldier_views import zeraki_api

import os

zeraki = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
zeraki.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "zeraki.db")}'
zeraki.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
zeraki.config['SECRET_KEY'] = 'zeraki-forces-secret'
zeraki.json.compact = False

db.init_app(zeraki)
migrate = Migrate(zeraki, db)
zeraki.register_blueprint(zeraki_api)

if __name__ == "__main__":
    zeraki.run()
    