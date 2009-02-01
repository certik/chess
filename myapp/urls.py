# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('myapp.views',
    (r'^$', 'list_people'),
    (r'^create/$', 'add_person'),
    (r'^show/(?P<key>.+)$', 'show_person'),
    (r'^edit/(?P<key>.+)$', 'edit_person'),
    (r'^delete/(?P<key>.+)$', 'delete_person'),
)
