# -*- coding: utf-8 -*-
from django.db.models import permalink
from google.appengine.ext import db

class Game(db.Model):
    """Some particular chess game."""
    white_player = db.StringProperty()
    black_player = db.StringProperty()
    moves = db.BlobProperty()
    owner = db.UserProperty()

    @permalink
    def get_absolute_url(self):
        return ('chess.views.show_game', (), {'key': self.key()})

class PGNFile(db.Model):
    """PGN file."""
    filename = db.StringProperty()
    filecontent = db.BlobProperty()
    owner = db.UserProperty()

    @permalink
    def get_absolute_url(self):
        return ('chess.views.show_pgn_file', (), {'key': self.key()})
