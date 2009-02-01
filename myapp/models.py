# -*- coding: utf-8 -*-
from django.db.models import permalink
from google.appengine.ext import db

class Person(db.Model):
    """Basic user profile with personal details."""
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)

    @permalink
    def get_absolute_url(self):
        return ('myapp.views.show_person', (), {'key': self.key()})
