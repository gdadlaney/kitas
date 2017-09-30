from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index/$', views.index, name='index'),
	url(r'^menu/$', views.menu, name='menu'),
	url(r'^blog/$', views.blog, name='blog'),
	url(r'^a$', views.test, name='test'),
	url(r'^b$', views.test2, name='test2'),
	url(r'^accounts$', views.accounts, name='accounts'),
	url(r'^posting$', views.post_form_upload,name='post_form_upload'),
]
