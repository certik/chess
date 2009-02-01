﻿# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('chess.views',
    (r'^$', 'list_games'),
    (r'^create/$', 'create_game'),
    (r'^show/(?P<key>.+)$', 'show_game'),
    (r'^edit/(?P<key>.+)$', 'edit_game'),
    (r'^delete/(?P<key>.+)$', 'delete_game'),
)
