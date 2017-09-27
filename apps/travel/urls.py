from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^register',views.register),
    url(r'^success',views.success),
    url(r'^login',views.login),
    url(r'^logout',views.logout),
    url(r'^addtrip',views.addtrip),
    url(r'^newtrip',views.newtrip),
    url(r'^travels/destination/(?P<id>[0-9]+)$',views.destination, name='destination'),
    url(r'^travels/destination/(?P<id>[0-9]+)/join$',views.join, name='join'),
]