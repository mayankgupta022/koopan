from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^coupons$', 'coupons.views.coupons', name='coupons'),
    url(r'^create$', 'coupons.views.create', name='create'),
    url(r'^update$', 'coupons.views.update', name='update'),
    url(r'^apply$', 'coupons.views.apply', name='apply'),
)
