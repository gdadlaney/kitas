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

def blog(request):
	return render(request, 'blog.html', {})

def category(request):
	return render(request, 'category.html', {})

def categories(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT name, description FROM rec_categories LIMIT 6")
		rec_category = list(cursor.fetchall())
		for i in range(rec_category.__len__()):
			rec_category[i] = list(rec_category[i])
	return render(request, 'categories.html', {'rec_category':rec_category})

def ingredients(request):
	return render(request, 'ingredients.html', {})

def accounts(request):
	return render(request, 'index.html/#cd-login', {})


def addIngredient(request):
	
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		with connection.cursor() as cursor:
			cursor.execute("SELECT name_english FROM ingredients")
			list_ingre = cursor.fetchall()

		return render(request, 'pingredients.html', {'list_ingre':list_ingre})


@csrf_protect
def recipe(request):
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		with connection.cursor() as cursor:
			cursor.execute("SELECT name_english FROM ingredients")
			list_ingre = cursor.fetchall()	
		return render(request, 'recipe.html', {'list_ingre':list_ingre})

@csrf_protect
def subRecipe(request):
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		data = request.POST
		name = data.get('name')
		pt = data.get('pt')
		ingre = data.getlist('ingre[]')
		servings = data.get('servings')
		directions = data.get('directions')
		category = data.get('category')
		# with connection.cursor() as cursor:
		print(ingre)
			
			# ingre = list(ingre)
			# for i in range(ingre.__len__()):
			# 	ingre[i] = list(ingre[i])
			# i=0
			# for i in range(ingre.__len__()):
			# 	cursor.execute("SELECT id FROM ingredients WHERE name_english='{0}' or name_hindi='{1}'".format(ingre[i], ingre[i]))
			# 	abc = cursor.fetchone()
			# 	cursor.execute("INSERT INTO recipes (name,directions,cust_id,servings,prep_time,category) VALUES('{0}', '{1}', {2}, '{3}', '{4}', {5})".format(name,directions,request.session['id'],servings,pt,category))#abc[0], qty))
			# 	cursor.execute("SELECT id FROM recipes WHERE name='{0}'".format(name))
			# 	xyz = cursor.fetchone()
			# 	cursor.execute("INSERT INTO rec_ingredients VALUES({0}, '{1}', '{2}', '{3}', {4})".format(xyz[0],qty,ingre[i],qty,abc[0]))

			# get the ingredients id from the input 
			# and insert in recipe
		# with connection.cursor as cursor:
		# 	cursor.execute("SELECT id FROM ingredients WHERE ")
		# 	cursor.execute("INSERT INTO recipes ")
		return render(request, 'recipe.html', {})


def pantry(request):	
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		with connection.cursor() as cursor:
			cursor.execute("SELECT ingr_id, qty FROM cust_ingredients WHERE cust_id={0}".format(request.session['id']))
			list_ingredient = list(cursor.fetchall())

			for i in range(list_ingredient.__len__()):
				list_ingredient[i] = list(list_ingredient[i])
			i = 0
			print(list_ingredient)
			for i in range(list_ingredient.__len__()):
				cursor.execute("SELECT name_english FROM ingredients WHERE id={0}".format(list_ingredient[i][0]))
				name = cursor.fetchone()
				list_ingredient[i][0] = name[0]
			print(list_ingredient)
		return render(request, 'pantry.html', {'list_ingredient':list_ingredient})




@csrf_protect
def listUp(request):
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		data = request.POST
		ingre = data.get('ingre')
		qty = data.get('qty')
		qty = int(''.join(filter(str.isdigit, qty)))
		with connection.cursor() as cursor:
			cursor.execute("SELECT id FROM ingredients WHERE name_english='{0}' or name_hindi='{1}'".format(ingre, ingre))
			abc = cursor.fetchone()

	
		
			cursor.execute("SELECT ingr_id FROM cust_ingredients WHERE ingr_id={0} and cust_id={1}".format(abc[0], request.session['id']))
			xyz = cursor.fetchone()
			if(xyz!=None and abc[0] == xyz[0]):
				cursor.execute("SELECT qty FROM cust_ingredients WHERE cust_id={0} and ingr_id={1}".format(request.session['id'], abc[0]))
				quan = cursor.fetchone()
				oqty = int(''.join(filter(str.isdigit, quan[0])))
				print(oqty)
				qty += oqty
				print(qty)
				cursor.execute("call up_list_of_ingredient({0}, {1}, '{2}')".format(request.session['id'], abc[0], qty))
			else:
				cursor.execute("call list_of_ingredient({0}, {1}, '{2}')".format(request.session['id'], abc[0], qty))
			return render(request, 'pingredients.html', {})



def breads(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT id FROM rec_categories WHERE name='{0}'".format("Breads"))
		id = cursor.fetchone()
		cursor.execute("SELECT name, directions FROM recipes WHERE category={0}".format(id[0]))
		recipes = cursor.fetchall()
		return render(request, 'events.html', {'recipes':recipes})


def snacks(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT id FROM rec_categories WHERE name='{0}'".format("Snacks"))
		id = cursor.fetchone()
		cursor.execute("SELECT name, directions FROM recipes WHERE category={0}".format(id[0]))
		recipes = cursor.fetchall()
		return render(request, 'events.html', {'recipes':recipes})



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
	return render(request, 'index.html', {"message":"Thank you, we miss you already "+user})

def test(request):
	return HttpResponse("Hello")

@csrf_exempt
def test2(request):
	# from django.db import connection

	# print (request.POST['data1'])
	# print (request.body)
	# return HttpResponse(request.body)
	"""
	arr = request.body.decode("utf-8")
	body = json.loads(arr)
	print (body)

	print("hi")
	arr = request.GET.getlist('data[]')
	print(arr)
	return HttpResponse(str(arr))
	"""
	
	data = request.POST
	ingr_list = data.getlist('ingr[]')
	print(ingr_list)
	user_ingredients_with_qty = {}
	for ingr in ingr_list:
		user_ingredients_with_qty.setdefault(ingr)

	print(user_ingredients_with_qty)
	#user_ingredients_with_qty = {'potato': 20, 'onion': 20, 'flour': 30}
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
	#sorted_list = [(1, [3, 1, 2]), (2, [1, 2]), (3, [1])]

	"""
	sorted_dict = {}
	for i in range(sorted_list.__len__()):
		sorted_dict[sorted_list[i][0]] = sorted_list[i][1];

	print("old sorted_dict = ", sorted_dict)
	#sorted_dict = {1: [3, 1, 2], 2: [1, 2], 3: [1]}
	

	with connection.cursor() as cursor:
		for key in sorted_dict:
			values = sorted_dict[key]
			qty_dict = {}
			for value in values:
				cursor.execute("select qty from rec_ingredients where rec_id=" + str(key) + " and ingr_id=" + str(value))
				rec_ingr_qty = cursor.fetchone()[0]
				usr_ingr_qty = user_ingredient_ids_with_qty[value]
				if(usr_ingr_qty >= rec_ingr_qty):
					qty_dict[value] = None
				else:
					qty_dict[value] = rec_ingr_qty - usr_ingr_qty
			sorted_dict[key] = qty_dict
	"""

	with connection.cursor() as cursor:
		for i in range(sorted_list.__len__()):
			sorted_list[i] = list(sorted_list[i])	#required, otherwise cannot change a tuple, i.e the ingredient list will not be converted to a dictionary

			rec_id = sorted_list[i][0]
			ingr_ids = sorted_list[i][1]
			qty_dict = {}
			for ingr_id in ingr_ids:
				cursor.execute("select qty from rec_ingredients where rec_id=" + str(rec_id) + " and ingr_id=" + str(ingr_id))
				rec_ingr_qty = cursor.fetchone()[0]
				usr_ingr_qty = user_ingredient_ids_with_qty[ingr_id]
				if(usr_ingr_qty >= rec_ingr_qty):
					qty_dict[ingr_id] = None
				else:
					qty_dict[ingr_id] = rec_ingr_qty - usr_ingr_qty
			
			sorted_list[i][1] = list(qty_dict.items())				#change
			for j in range(sorted_list[i][1].__len__()):			#change
				sorted_list[i][1][j] = list(sorted_list[i][1][j])

	print("sorted_list = ", sorted_list)
	#sorted_list =  [[1, {1: None, 2: None, 3: None}], [2, {1: 5, 2: None}], [3, {1: 25}]]


	final_str = ""
	final_str += str(sorted_list) + "<br><br>"

	"""
	for i in range(recipes_matching.__len__()):
		final_str += str(sorted_list[i][0]) + " : " + str(sorted_list[i][1]) + "<br>" 
	"""
	"""#for dictionary
	#sorted_list =  [[1, {1: None, 2: None, 3: None}], [2, {1: 5, 2: None}], [3, {1: 25}]]	
	with connection.cursor() as cursor:
		for i in range(sorted_list.__len__()):
			final_str += "recipe id = " + str(sorted_list[i][0]) + " : " + str(
				sorted_list[i][1].__len__()) + " ingredients matched" + "<br>"
			final_str += "ingredients available: <br>"
			for temp in sorted_list[i][1]:
				cursor.execute("select name_english from ingredients where id=" + str(temp))
				ingr = cursor.fetchone()
				final_str += ingr[0] + "<br>"
			cursor.execute("select name, directions from recipes where id=" + str(sorted_list[i][0]))
			recipe_desc = cursor.fetchone()
			#print("recipe_desc = ", recipe_desc)
			final_str += recipe_desc[0] + "<br>" + recipe_desc[1] + "<br><br>"
	"""


	# sorted_list =  [[1, [(1, None), (2, None), (3, None)]], [2, [(1, 5), (2, None)]], [3, [(1, 25)]]]
	with connection.cursor() as cursor:
		for i in range(sorted_list.__len__()):
			recipe_list = []
			final_str += "recipe id = " + str(sorted_list[i][0]) + " : " + str(
				sorted_list[i][1].__len__()) + " ingredients matched" + "<br>"
			final_str += "ingredients available: <br>"

			recipe_id = sorted_list[i][0]
			cursor.execute("select name, directions from recipes where id=" + str(recipe_id))
			recipe_desc = cursor.fetchone()
			sorted_list[i][0] = list(recipe_desc)

			for j in range(sorted_list[i][1].__len__()):
				temp = sorted_list[i][1][j]
				ingredient_id1 = temp[0]
				cursor.execute("select name_english from ingredients where id=" + str(ingredient_id1))
				ingredient_name1 = cursor.fetchone()[0]

				sorted_list[i][1][j][0] = ingredient_name1

				final_str += ingredient_name1 + "<br>"
			
			#print("recipe_desc = ", recipe_desc)
			final_str += recipe_desc[0] + "<br>" + recipe_desc[1] + "<br><br>"

	print()
	print(sorted_list)
	print()
	print(final_str)
	
	"""
	recipe_details = []
	recipe_ingredients = []

	with connection.cursor() as cursor:
		for i in range(sorted_list.__len__()):
			cursor.execute("select name, directions from recipes where id=" + str(sorted_list[i][0]))
			rec_details = list(cursor.fetchall())
			cursor.execute("select ingr_string, qty from rec_ingredients where rec_id=" + str(sorted_list[i][0]))		#check
			rec_ingredients = list(cursor.fetchall())

			recipe_details.append(recipe_details)
			recipe_ingredients.append(rec_ingredients)

	print("***", recipe_details)
	print("***", recipe_ingredients)
	"""

	#return render(request, 'blog.html', {'sorted_list': sorted_list, 'recipe_details':recipe_details, 'recipe_ingredients':rec_ingredients})
	return HttpResponse(str(sorted_list))

	#[[('recipe 1', '...'), [['potato', None], ['onion', None], ['flour', None]]], [('recipe 2', '...'), [['potato', 5], ['onion', None]]], [('recipe 3', '...'), [['potato', 25]]]]
	

	#return render(request, 'blog.html', {"sorted_list": sorted_list})


def customers(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT name FROM customers")
		row = cursor.fetchone()
	return HttpResponse(row)


