from flask_login import UserMixin
from sqlalchemy import Table

from dashboard.extensions import db
from dashboard.extensions import login


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(150))


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
