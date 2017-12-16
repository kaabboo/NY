# APP2 URLS
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^new$', views.new),    
    url(r'^create$', views.create),
    url(r'^(?P<trip_id>\d+)/read$', views.read),
    url(r'^(?P<trip_id>\d+)/update$', views.update),
]