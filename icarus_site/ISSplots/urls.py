from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.plot, name='plot'),
	url(r'^api/getTLE', views.getTLE, name='getTLE'),
]
