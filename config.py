from dotenv import load_dotenv
import os

# Charge les variables d'environnement depuis le fichier .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    def __init__(self):
        if self.SQLALCHEMY_DATABASE_URI is None:
            log.warn(CONFIG, "DATABASE_URL is not set in .env file")