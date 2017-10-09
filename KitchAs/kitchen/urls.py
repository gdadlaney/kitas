from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index$', views.index, name='index'),
	url(r'^contact$', views.contact, name='contact'),
	url(r'^blog$', views.blog, name='blog'),
	url(r'^search_result$', views.search_result, name='search_result'),
	#url(r'^search_result/(?P<is_redirected>[A-Za-z\s()]+)$', views.search_result, name='search_result'),		#check
	url(r'^logout$', views.logout, name='logout'),
	url(r'^signup$', views.signup, name='signup'),
	url(r'^login$', views.login, name='login'),
	url(r'^categories$', views.categories, name='categories'),
	url(r'^ingredients$', views.ingredients, name='ingredients'),
	url(r'^list$', views.addIngredient, name="addIngredient"),
	url(r'^listup$', views.listUp, name="listUp"),
	url(r'^recipe$', views.recipe, name="recipe"),
	url(r'^pantry$', views.pantry, name="pantry"),
	url(r'^myrecipe$', views.myrecipe, name="myrecipe"),
	url(r'^category/(?P<rec_name>[A-Za-z()\s ]+)$', views.category, name="category"),
	url(r'^makearecipe/(?P<rec_name>[A-Za-z()\s ]+)$', views.makearecipe, name="makearecipe"),
	url(r'^single/(?P<rec_name>[A-Za-z()\s ]+)$', views.single, name="single"),
	url(r'^subrecipe$', views.subRecipe, name="subRecipe"),
	url(r'^delrecipe$', views.delRecipe, name="delRecipe"),
	url(r'^delrecipeuser/(?P<rec_name>[A-Za-z()\s ]+)$', views.delRecipeUser, name="delRecipeUser"),
	#url(r'^', views.index, name='index'),
	url(r'^admin$', views.admin, name="admin"),
	url(r'^', views.page_not_found, name='page_not_found'),
]

