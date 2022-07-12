""" Main Module """
from os import environ
from sys import (exit, stdout)
from flask import Flask
from flask_sqlalchemy import (SQLAlchemy)
from flask_migrate import Migrate
from flask_cors import CORS
from flask_graphql import GraphQLView
import logging

APP = Flask(__name__)
CORS(APP)
APP.config.from_pyfile('settings.py')

logging.basicConfig(stream=stdout,
                    level=APP.config['LOG_LEVEL'])

logging.info('Starting ...')
logging.info(APP.config['SQLALCHEMY_URI'])

DB = SQLAlchemy(APP)

MIGRATE = Migrate(APP, DB)

from .schema import SCHEMA

@APP.route('/')
def health():
    return 'healthy'


APP.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=SCHEMA,
        graphiql=APP.config['GRAPHIQL'],
        get_context=lambda: {'session': DB.session}
    )
)