from flask_cors import CORS
from flask import Flask

from controllers.tournamentController import tournamentBp
from controllers.matchController import matchBp
from controllers.teamController import teamBp
from config import Config
from database import db

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(tournamentBp)
app.register_blueprint(matchBp)
app.register_blueprint(teamBp)

# Création des tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()