from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    url(r'^create$', 'koopan.views.create', name='create'),
    url(r'^update$', 'koopan.views.update', name='update'),
    url(r'^apply$', 'koopan.views.apply', name='apply'),
)
