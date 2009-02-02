# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('chess.views',
    (r'^$', 'list_games'),
    (r'^create/$', 'create_game'),
    (r'^show/(?P<key>.+)$', 'show_game'),
    (r'^edit/(?P<key>.+)$', 'edit_game'),
    (r'^delete/(?P<key>.+)$', 'delete_game'),
    (r'^upload/$', 'upload_pgn'),
    (r'^showpgn/(?P<key>.+)$', 'show_pgn_file'),
    (r'^deletepgn/(?P<key>.+)$', 'delete_pgn_file'),
    (r'^updatemoves/(?P<key>.+)$', 'update_moves'),
    (r'^logout/$', 'logout'),
)
