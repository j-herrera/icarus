from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.map, name='map'),
	url(r'^mapSim', views.mapSim, name='mapSim'),
	url(r'^api/getPos', views.getPos, name='getPos'),
	url(r'^api/getProjAndPos', views.getProjAndPos, name='getProjAndPos'),
]
