import sqlite3
from sqlalchemy import create_engine, Table
from flask_sqlalchemy import SQLAlchemy

import configparser

from flask_login import LoginManager, UserMixin
from db.users_table_setup import Users

import dash_bootstrap_components as dbc

from flask import Flask
from dash import Dash


server = Flask(__name__)
server.config.update(
        SECRET_KEY='ToBeChanged1234!',
        SQLALCHEMY_DATABASE_URI='sqlite:///C:/Users/adamk/Documents/Kursy/Python/AtlasGrzybow/database/users.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
)


conn = sqlite3.connect('C:/Users/adamk/Documents/Kursy/Python/AtlasGrzybow/database/users.sqlite')
engine = create_engine('sqlite:///C:/Users/adamk/Documents/Kursy/Python/AtlasGrzybow/database/users.sqlite')
db = SQLAlchemy()

config = configparser.ConfigParser()

db.init_app(server)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

Users_tbl = Table('users', Users.metadata)

class Users(UserMixin, Users):
    pass


login_manager = LoginManager()
login_manager.init_app(server)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    dbc.themes.MORPH
]
app = Dash(
        __name__,
        server=server,
        suppress_callback_exceptions=True,
        external_stylesheets=[external_stylesheets[0]]
)

app.title = "Atlas Grzybów"


