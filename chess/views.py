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

from google.appengine.api import users
from google.appengine.ext import db

def render_to_response(tempname, dictionary):
    """
    For some reason the django.shortcuts.render_to_response() is not working
    properly.
    """
    t = loader.get_template(tempname)
    c = Context(dictionary)
    r = HttpResponse(t.render(c), mimetype="application/xhtml+xml")
    return r

def BREAKPOINT():
    import pdb, sys
    p = pdb.Pdb(None, sys.__stdin__, sys.__stdout__)
    p.set_trace()

def login_required(func):
    """Decorator that redirects to the login page if you're not logged in."""
    def login_wrapper(request, *args, **kwds):
        if users.get_current_user() is None:
            return HttpResponseRedirect(users.create_login_url(request.path))
        return func(request, *args, **kwds)
    return login_wrapper


@login_required
def list_games(request):
    u = users.get_current_user()
    games = db.Query(Game).filter("owner", u)
    pgn_files = db.Query(PGNFile).filter("owner", u)
    nick = users.get_current_user().nickname()
    return render_to_response("game_list.html", {
        "games": games,
        "pgn_files": pgn_files,
        "login": nick,
        })
    #return object_list(request, Game.all(), paginate_by=10)

@login_required
def show_game(request, key):
    return object_detail(request, Game.all(), key)

class CreateGameForm(forms.Form):
    white_player = forms.CharField(max_length=50)
    black_player = forms.CharField(max_length=50)

@login_required
def create_game(request):
    if request.method == "POST":
        form = CreateGameForm(request.POST, request.FILES)
        if form.is_valid():
            p = Game(white_player=form.cleaned_data["white_player"],
                    black_player=form.cleaned_data["black_player"],
                    owner=users.get_current_user())
            p.put()
            return HttpResponseRedirect(reverse("chess.views.list_games"))
    else:
        form = CreateGameForm()
    return render_to_response("game_form.html", {"form": form})

@login_required
def edit_game(request, key):
    return update_object(request, Game, key)

@login_required
def delete_game(request, key):
    return delete_object(request, Game, object_id=key,
        post_delete_redirect=reverse('chess.views.list_games'))

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()

@login_required
def upload_pgn(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            p = PGNFile(filename=f.name, filecontent=f.read(),
                    owner=users.get_current_user())
            p.put()
            return HttpResponseRedirect(reverse("chess.views.list_games"))
    else:
        form = UploadFileForm()
    return render_to_response("pgnfile_form.html", {"form": form})

@login_required
def show_pgn_file(request, key):
    return object_detail(request, PGNFile.all(), key)

@login_required
def delete_pgn_file(request, key):
    return delete_object(request, PGNFile, object_id=key,
        post_delete_redirect=reverse('chess.views.list_games'))

def logout(request):
    return HttpResponseRedirect(users.create_logout_url("/"))
