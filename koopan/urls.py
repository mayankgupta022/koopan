from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'koopan.views.home', name='home'),
    url(r'^api/', include('coupons.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
