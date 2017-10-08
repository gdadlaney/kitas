from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index$', views.index, name='index'),
	url(r'^contact$', views.contact, name='contact'),
	url(r'^blog$', views.blog, name='blog'),
	url(r'^search_for_recipes$', views.search_for_recipes, name='search_for_recipes'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^signup$', views.signup, name='signup'),
	url(r'^login$', views.login, name='login'),
	url(r'^categories$', views.categories, name='categories'),
	url(r'^ingredients$', views.ingredients, name='ingredients'),
	url(r'^list$', views.addIngredient, name="addIngredient"),
	url(r'^listup$', views.listUp, name="listUp"),
	url(r'^recipe$', views.recipe, name="recipe"),
	url(r'^pantry$', views.pantry, name="pantry"),
	url(r'^Breads$', views.breads, name="breads"),
	url(r'^Snacks$', views.snacks, name="snacks"),
	url(r'^makearecipe/(?P<rec_name>[A-Z]+)$', views.makearecipe, name="makearecipe"),
	url(r'^single/(?P<rec_name>[A-Z]+)$', views.single, name="single"),
	url(r'^subrecipe$', views.subRecipe, name="subRecipe"),
	#url(r'^', views.index, name='index'),
	url(r'^', views.page_not_found, name='page_not_found'),
]

