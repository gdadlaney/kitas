import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import UpdateView, ListView
from django.db import connection
from django.views.decorators.csrf import csrf_protect ,csrf_exempt


def page_not_found(request):
	return render(request, 'page_not_found.html', {"error_message": "The URL that you requested was not found"})

def index(request):
	return render(request, 'index.html', {})

def menu(request):
	return render(request, 'menu.html', {})

def blog(request):
	# sorted_list = [[['recipe 1', '...'], [['potato', None], ['onion', None], ['flour', None]]], [['recipe 2', '...'], [['potato', 5], ['onion', None]]], [['recipe 3', '...'], [['potato', 25]]]]
	# return render(request, 'blog.html', {"sorted_list": sorted_list})
	return render(request, 'blog.html', {})

def category(request):
	return render(request, 'category.html', {})

def categories(request):
	return render(request, 'categories.html', {})

def ingredients(request):
	return render(request, 'ingredients.html', {})

def accounts(request):
	return render(request, 'index.html/#cd-login', {})


def addIngredient(request):
	return render(request, 'pingredients.html', {})


@csrf_protect
def listUp(request):
	data = request.POST
	ingre = data.get('ingre')
	qty = data.get('qty')
	with connection.cursor() as cursor:
		cursor.execute("SELECT id FROM ingredients WHERE name_english={0} or name_hindi={1}".format(ingre, ingre))
		abc = cursor.fetchone()
		cursor.execute("INSERT INTO cust_ingredients VALUES({0}, {1}, {2})".format(request.session['id'], abc[0], qty))
	return render(request, 'pingredients.html', {})

@csrf_protect
def login(request):
	data = request.POST
	email = data.get('email')
	passw = data.get('password')
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM customers WHERE email='{0}' and password='{1}'".format(email, passw))
		abc = cursor.fetchone()
	request.session['id'] = abc[0]
	request.session['user'] = abc[1]
	return render(request, 'index.html', {})

@csrf_protect
def signup(request):
	data = request.POST
	name = data.get('name')
	email = data.get('email')
	passw = data.get('password')
	passwd = data.get('cpassword')
	print(name, email, passw, passwd)
	if (email=="" or  name=="" or passw!=passwd):
		return HttpResponse("All Fields are compulsory")
	else:
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO customers(name, email, password) values('{0}', '{1}', '{2}')".format(name, email, passw))
		return HttpResponse("Record Inserted")

def logout(request):
	if request.session['user'] != None:
		user = request.session['user']
	else:
		user = " "
	request.session['user']=None
	return render(request, 'index.html', {"abc":"Thank you, we miss you already "+user})

def test(request):
	return HttpResponse("Hello")

@csrf_exempt
def test2(request):
	# from django.db import connection

	# print (request.POST['data1'])
	# print (request.body)
	# return HttpResponse(request.body)
	arr = request.body.decode("utf-8")
	body = json.loads(arr)
	print (body)

	# user_ingredients_with_qty = {'potato': 20, 'onion': 20, 'flour': 30}
	# # user_ingredients_with_qty = {'potato':None, 'onion':None, 'flour':None}	#for user type 3

	# user_ingredients = list(user_ingredients_with_qty.keys())
	# user_qty = list(user_ingredients_with_qty.values())
	# # user_ingredients = ['potato', 'onion', 'flour']
	# user_ingredient_ids = []
	# user_ingredient_ids_with_qty = {}

	# # converts ingredient name to ingredient_id
	# with connection.cursor() as cursor:
	# 	for i in range(user_ingredients.__len__()):
	# 		# cursor.execute("select id from ingredients where name_english='%s'", user_ingredients[i]) does not work
	# 		cursor.execute("select id from ingredients where name_english='" + user_ingredients[i] + "' or name_hindi='" + user_ingredients[i] + "'")
	# 		ingredient_id = int(cursor.fetchone()[0])									#'NoneType' object is not subscriptable - if db missing
	# 		user_ingredient_ids.append(ingredient_id)
	# 		user_ingredient_ids_with_qty[ ingredient_id ] = user_qty[i]		#check

	# print("user_ingredient_ids = ", user_ingredient_ids)
	# # user_ingredients = [1, 2, 3]	#from the checkboxes, will names be mapped to ids?
	# print("user_ingredient_ids_with_qty = ", user_ingredient_ids_with_qty)
	# # user_ingredient_ids_with_qty = {1: 30, 2: 30, 3: 30}

	# recipes_matching = []

	# with connection.cursor() as cursor:
	# 	for i in range(user_ingredients.__len__()):
	# 		# cursor.execute("select rec_id from rec_ingredients where ingr_id="+str(user_ingredient_ids[i]))
	# 		cursor.execute(
	# 			"select rec_id from rec_ingredients where ingr_id=" + str(user_ingredient_ids[i]))
	# 		recipes = list(cursor.fetchall()) 	# how to correct this format? - ((1,), (2,), (3,))
	# 		#print(recipes)
	# 		recipes_matching.append(recipes)

	# print("old recipes_matching = ", recipes_matching)
	# # recipes_matching - [((1,), (2,), (3,)), ((1,), (2,)), ((1,),)]

	# # look for a better way to convert tuples to ints
	# for i in range(recipes_matching.__len__()):
	# 	for j in range(recipes_matching[i].__len__()):
	# 		recipes_matching[i][j] = recipes_matching[i][j][0]

	# print("recipes_matching = ", recipes_matching)

	# # recipes_matching - [[1, 2, 3], [1, 2], [1]]

	# def ingredients_present(user_ingredients, recipes_matching):
	# 	dict = {}
	# 	for i in range(user_ingredients.__len__()):
	# 		for temp in recipes_matching[i]:
	# 			keys = dict.setdefault(temp, [])	# adds key to dict & assigns a default value, if key not found in dict
	# 			keys.append(user_ingredients[i])
	# 	return dict

	# dict = {}

	# dict = ingredients_present(user_ingredient_ids, recipes_matching)
	# print("dict = ", dict)

	# """
	# for i in range(recipes_matching.__len__()):
	# 	for j in range(recipes_matching[i].__len__()):
	# 		if(not dict.__contains__(recipes_matching[i][j])):
	# 			dict[recipes_matching[i][j]] = 1
	# 		else:
	# 			dict[recipes_matching[i][j]] += 1
	# """

	# # sorting the dict in reverse order
	# # import operator
	# # sorted_list = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)

	# # sorting list according
	# sorted_list = sorted(dict.items(), key=lambda elem: elem[1].__len__(), reverse=True)

	# print("sorted_list = ", sorted_list)
	# #sorted_list = [(1, [3, 1, 2]), (2, [1, 2]), (3, [1])]

	# """
	# sorted_dict = {}
	# for i in range(sorted_list.__len__()):
	# 	sorted_dict[sorted_list[i][0]] = sorted_list[i][1];

	# print("old sorted_dict = ", sorted_dict)
	# #sorted_dict = {1: [3, 1, 2], 2: [1, 2], 3: [1]}


	# arr = request.GET.getlist('data[]')
	# print(arr)
	# return HttpResponse(str(arr))
	print("hi")
	arr = request.GET.getlist('data[]')
	print(arr)
	return HttpResponse(str(arr))

	user_ingredients_with_qty = {'potato': 20, 'onion': 20, 'flour': 30}
	# user_ingredients_with_qty = {'potato':None, 'onion':None, 'flour':None}	#for user type 3

	user_ingredients = list(user_ingredients_with_qty.keys())
	user_qty = list(user_ingredients_with_qty.values())
	# user_ingredients = ['potato', 'onion', 'flour']
	user_ingredient_ids = []
	user_ingredient_ids_with_qty = {}

	# converts ingredient name to ingredient_id
	with connection.cursor() as cursor:
		for i in range(user_ingredients.__len__()):
			# cursor.execute("select id from ingredients where name_english='%s'", user_ingredients[i]) does not work
			cursor.execute("select id from ingredients where name_english='" + user_ingredients[i] + "' or name_hindi='" + user_ingredients[i] + "'")
			ingredient_id = int(cursor.fetchone()[0])									#'NoneType' object is not subscriptable - if db missing
			user_ingredient_ids.append(ingredient_id)
			user_ingredient_ids_with_qty[ ingredient_id ] = user_qty[i]		#check

	print("user_ingredient_ids = ", user_ingredient_ids)
	# user_ingredients = [1, 2, 3]	#from the checkboxes, will names be mapped to ids?
	print("user_ingredient_ids_with_qty = ", user_ingredient_ids_with_qty)
	# user_ingredient_ids_with_qty = {1: 30, 2: 30, 3: 30}

	recipes_matching = []

	with connection.cursor() as cursor:
		for i in range(user_ingredients.__len__()):
			# cursor.execute("select rec_id from rec_ingredients where ingr_id="+str(user_ingredient_ids[i]))
			cursor.execute(
				"select rec_id from rec_ingredients where ingr_id=" + str(user_ingredient_ids[i]))
			recipes = list(cursor.fetchall()) 	# how to correct this format? - ((1,), (2,), (3,))
			#print(recipes)
			recipes_matching.append(recipes)

	print("old recipes_matching = ", recipes_matching)
	# recipes_matching - [((1,), (2,), (3,)), ((1,), (2,)), ((1,),)]

	# look for a better way to convert tuples to ints
	for i in range(recipes_matching.__len__()):
		for j in range(recipes_matching[i].__len__()):
			recipes_matching[i][j] = recipes_matching[i][j][0]

	print("recipes_matching = ", recipes_matching)

	# recipes_matching - [[1, 2, 3], [1, 2], [1]]

	def ingredients_present(user_ingredients, recipes_matching):
		dict = {}
		for i in range(user_ingredients.__len__()):
			for temp in recipes_matching[i]:
				keys = dict.setdefault(temp, [])	# adds key to dict & assigns a default value, if key not found in dict
				keys.append(user_ingredients[i])
		return dict

	dict = {}

	dict = ingredients_present(user_ingredient_ids, recipes_matching)
	print("dict = ", dict)

	"""
	for i in range(recipes_matching.__len__()):
		for j in range(recipes_matching[i].__len__()):
			if(not dict.__contains__(recipes_matching[i][j])):
				dict[recipes_matching[i][j]] = 1
			else:
				dict[recipes_matching[i][j]] += 1
	"""

	# sorting the dict in reverse order
	# import operator
	# sorted_list = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)

	# sorting list according
	sorted_list = sorted(dict.items(), key=lambda elem: elem[1].__len__(), reverse=True)

	print("sorted_list = ", sorted_list)


def customers(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT name FROM customers")
		row = cursor.fetchone()
	return HttpResponse(row)


