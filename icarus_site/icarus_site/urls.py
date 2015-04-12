from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'icarus_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^$', 'home.views.index', name='home'),
	url(r'^ISStrace/', include('ISStrace.urls')),
	url(r'^ISSplots/', include('ISSplots.urls')),
	url(r'^ISS3D/', include('ISS3D.urls')),
	url(r'^admin/', include(admin.site.urls)),
]

handler404 = 'icarus_site.views.handler404'
