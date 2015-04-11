from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'icarus_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^ISStrace/', include('ISStrace.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
