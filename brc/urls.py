from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'brc.views.index'),
	url(r'^login', 'brc.views.authenticate_login'),
	
	url(r'^readings/', include('readings.urls'))
    # Examples:
    # url(r'^$', 'brc.views.home', name='home'),
    # url(r'^brc/', include('brc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
