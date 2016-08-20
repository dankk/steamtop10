from django.conf.urls import *

import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^steam/results/$', views.results, name='results'),
]