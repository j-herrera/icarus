from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.Dplot, name='Dplot'),
	url(r'^api/getTLE', views.getTLE, name='getTLE'),
	url(r'^api/getJ2TLE', views.getJ2TLE, name='getJ2TLE'),
	url(r'^Dsym', views.Dsym, name='Dsym'),
]
