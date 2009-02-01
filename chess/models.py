# -*- coding: utf-8 -*-
from django.db.models import permalink
from google.appengine.ext import db

class Game(db.Model):
    """Some particular chess game."""
    white_player = db.StringProperty(required=False)
    black_player = db.StringProperty(required=False)
    moves = db.StringProperty(required=False)

    @permalink
    def get_absolute_url(self):
        return ('chess.views.show_game', (), {'key': self.key()})
