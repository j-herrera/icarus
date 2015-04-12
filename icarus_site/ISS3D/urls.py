from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.Dplot, name='Dplot'),
	url(r'^api/getTLE', views.getTLE, name='getTLE'),
]
