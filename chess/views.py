# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, \
    update_object
from chess.models import Game, PGNFile
from ragendja.template import render_to_response, render_to_string

def list_games(request):
    return object_list(request, Game.all(), paginate_by=10)

def show_game(request, key):
    return object_detail(request, Game.all(), key)

def create_game(request):
    return create_object(request, Game)

def edit_game(request, key):
    return update_object(request, Game, key)

def delete_game(request, key):
    return delete_object(request, Game, object_id=key,
        post_delete_redirect=reverse('chess.views.list_games'))

def upload_pgn(request):
    return create_object(request, PGNFile)

def show_pgn_file(request, key):
    return object_detail(request, PGNFile.all(), key)

def delete_pgn_file(request, key):
    return delete_object(request, PGNFile, object_id=key,
        post_delete_redirect=reverse('chess.views.list_games'))
