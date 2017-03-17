
import datetime
import logging
import os
import socket

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


app = Flask(__name__)

# Environment variables are defined in app.yaml.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Aspect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created = db.Column(db.DateTime())
    creator = db.Column(db.Integer(10))

    def __init__(self, name, description, creator):
        self.name = name
        self.description = description
        self.creator = creator
        self.created = datetime.datetime.now()
