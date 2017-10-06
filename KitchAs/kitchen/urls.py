from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index$', views.index, name='index'),
	url(r'^menu2$', views.menu2, name='menu2'),
	url(r'^menu$', views.menu, name='menu'),
	url(r'^blog$', views.blog, name='blog'),
	url(r'^a$', views.test, name='test'),
	url(r'^b$', views.test2, name='test2'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^signup$', views.signup, name='signup'),
	url(r'^login$', views.login, name='login'),
	url(r'^categories$', views.categories, name='categories'),
	url(r'^ingredients$', views.ingredients, name='ingredients'),
	url(r'^list$', views.addIngredient, name="addIngredient"),
	url(r'^listUp$', views.listUp, name="listUp"),
	#url(r'^', views.index, name='index'),
	url(r'^', views.page_not_found, name='page_not_found'),
]

