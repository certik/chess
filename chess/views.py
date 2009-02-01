# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, \
    update_object
#from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django import forms

from chess.models import Game, PGNFile
from ragendja.template import render_to_response, render_to_string

def render_to_response(tempname, dictionary):
    """
    For some reason the django.shortcuts.render_to_response() is not working
    properly.
    """
    t = loader.get_template(tempname)
    c = Context(dictionary)
    r = HttpResponse(t.render(c), mimetype="application/xhtml+xml")
    return r

def list_games(request):
    return render_to_response("game_list.html",
            {"games": Game.all(), "pgn_files": PGNFile.all()})
    #return object_list(request, Game.all(), paginate_by=10)

def show_game(request, key):
    return object_detail(request, Game.all(), key)

def create_game(request):
    return create_object(request, Game)

def edit_game(request, key):
    return update_object(request, Game, key)

def delete_game(request, key):
    return delete_object(request, Game, object_id=key,
        post_delete_redirect=reverse('chess.views.list_games'))

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()

def upload_pgn(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect(reverse("chess.views.list_games"))
    else:
        form = UploadFileForm()
    return render_to_response("pgnfile_form.html", {"form": form})

def show_pgn_file(request, key):
    return object_detail(request, PGNFile.all(), key)

def delete_pgn_file(request, key):
    return delete_object(request, PGNFile, object_id=key,
        post_delete_redirect=reverse('chess.views.list_games'))
