# -*- coding: utf-8 -*-
from django.db.models import permalink
from google.appengine.ext import db

class Person(db.Model):
    """Basic user profile with personal details."""
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)

    @permalink
    def get_absolute_url(self):
        return ('chess.views.show_person', (), {'key': self.key()})

class Game(db.Model):
    """Basic user profile with personal details."""
    white_player = db.StringProperty(required=True)
    black_player = db.StringProperty(required=True)
    moves = db.StringProperty(required=True)
