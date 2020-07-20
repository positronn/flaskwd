# app/models.py
from . import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)

    def __repr__(self):
        return fr'<Role {self.name}>'
    
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)

    def __repr__(self):
        return fr'<User {self.username}>'
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # user password
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
