from django.conf.urls import patterns, url
from firmas import views

urlpatterns = patterns ('',
	url(r'^$', views.home, name='home'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^firma/$', views.firma, name='firma'),
	url(r'^save_signature/$', views.save_signature, name='save_signature'),
	url(r'^firma/(?P<signature_id>[0-9]+)/$', views.signature, name='signature'),
)