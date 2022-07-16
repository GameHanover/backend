from os import getenv

APP_NAME = 'games'
# Default to info
LOG_LEVEL = getenv("LOG_LEVEL") or 20

SQLALCHEMY_URI = getenv("SQLALCHEMY_URI")
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_URI

SECRET_KEY = getenv('SECRET_KEY', 'my_secret')
SECRET_TIMEOUT = int(getenv('SECRET_TIMEOUT', '900'))
DEBUG = getenv('DEBUG', False)
TESTING = getenv('TESTING', False)
BCRYPT_LOG_ROUNDS = 13

GRAPHIQL = getenv('GRAPHIQL', False)
