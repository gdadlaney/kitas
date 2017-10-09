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

'''
#angular js categories
def category(request):
	return render(request, 'category.html', {})
'''

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


def makearecipe(request, rec_name):
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		with connection.cursor() as cursor:
			cursor.execute("SELECT ingr_id, qty FROM cust_ingredients WHERE cust_id={0}".format(request.session['id']))
			data_list = cursor.fetchall()
			cursor.execute("SELECT id FROM recipes WHERE name='{0}'".format(rec_name))
			rec_id = cursor.fetchone()[0]
			cursor.execute("SELECT ingr_id, qty FROM rec_ingredients WHERE rec_id={0}".format(rec_id))
			list_ingre_w_qty = cursor.fetchall()
			
			for i in range(data_list.__len__()):
				for j in range(list_ingre_w_qty.__len__()):
					if data_list[i][0]==list_ingre_w_qty[j][0]:
						qt1 = convert_qty( data_list[i][1])
						qt2 = convert_qty( list_ingre_w_qty[j][1])

						if(list_ingre_w_qty[j][1]!=None and qt1[1]==qt[2]):
							rqty = int(''.join(filter(str.isdigit, data_list[i][1]))) - int(''.join(filter(str.isdigit, list_ingre_w_qty[j][1]))) 
							if rqty <= 0:
								cursor.execute("DELETE FROM cust_ingredients WHERE cust_id={0} and ingr_id={1}".format(request.session['id'], data_list[i][0]))
							else:
								cursor.execute("UPDATE cust_ingredients SET qty={0} WHERE cust_id={1} and ingr_id={2}".format(rqty, request.session['id'], data_list[i][0]))
			
			cursor.execute("SELECT ingr_id, qty FROM cust_ingredients WHERE cust_id={0}".format(request.session['id']))
			list_ingredient = list(cursor.fetchall())

			for i in range(list_ingredient.__len__()):
				list_ingredient[i] = list(list_ingredient[i])
			
			for i in range(list_ingredient.__len__()):
				cursor.execute("SELECT name_english FROM ingredients WHERE id={0}".format(list_ingredient[i][0]))
				name = cursor.fetchone()
				list_ingredient[i][0] = name[0]
		return render(request, 'pantry.html', {'list_ingredient':list_ingredient})


@csrf_protect
def recipe(request):
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		with connection.cursor() as cursor:
			cursor.execute("SELECT name_english FROM ingredients")
			list_ingre = cursor.fetchall()	
		return render(request, 'recipe.html', {'list_ingre':list_ingre})


def single(request, rec_name):
	with connection.cursor() as cursor:
		cursor.execute("SELECT name, directions, time_modified FROM recipes where name='{0}'".format(rec_name))
		recipe_info = cursor.fetchone()
		print(recipe_info)
	return render(request, 'single.html', {'recipe_info':recipe_info})

#add user recipes
@csrf_protect
def subRecipe(request):
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		data = request.POST
		name = data.get('name')
		pt = data.get('pt')
		ingre = data.getlist('ingre[]')
		qty = data.getlist('qty[]')
		servings = data.get('servings')
		directions = data.get('directions')
		category = data.get('category')
		print(data)
		with connection.cursor() as cursor:
			cursor.execute("SELECT name_english FROM ingredients")
			list_ingre = cursor.fetchall()
			ingre = list(ingre)
			qty = list(qty)
			# for i in range(ingre.__len__()):
			# 	ingre[i] = list(ingre[i])
			# 	qty[i] = list(qty[i])
			# i=0
			cursor.execute("INSERT INTO recipes (name,directions,cust_id,servings,prep_time,category) VALUES('{0}', '{1}', {2}, '{3}', '{4}', {5})".format(name,directions,request.session['id'],servings,pt,category))#abc[0], qty))
			cursor.execute("SELECT id FROM recipes WHERE name='{0}'".format(name))
			xyz = cursor.fetchone()
			for i in range(ingre.__len__()):
				cursor.execute("SELECT id FROM ingredients WHERE name_english='{0}' or name_hindi='{1}'".format(ingre[i], ingre[i]))
				abc = cursor.fetchone()
				cursor.execute("INSERT INTO rec_ingredients VALUES({0}, '{1}', '{2}', '{3}', {4})".format(xyz[0],qty[i],ingre[i],qty[i],abc[0]))


			# get the ingredients id from the input 
			# and insert in recipe
		# with connection.cursor as cursor:
		# 	cursor.execute("SELECT id FROM ingredients WHERE ")
		# 	cursor.execute("INSERT INTO recipes ")
		return render(request, 'recipe.html', {'list_ingre':list_ingre})


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



#add ingredients to pantry
@csrf_protect
def listUp(request):
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		data = request.POST
		ingre = data.get('ingre')
		qty = data.get('qty')
		if(qty!=""):
			qty = int(''.join(filter(str.isdigit, qty)))
		else:
			qty= 0
		with connection.cursor() as cursor:
			cursor.execute("SELECT name_english FROM ingredients")
			list_ingre = cursor.fetchall()
			cursor.execute("SELECT id FROM ingredients WHERE name_english='{0}' or name_hindi='{1}'".format(ingre, ingre))
			abc = cursor.fetchone()
			cursor.execute("SELECT ingr_id FROM cust_ingredients WHERE ingr_id={0} and cust_id={1}".format(abc[0], request.session['id']))
			xyz = cursor.fetchone()
			if(xyz!=None and abc[0] == xyz[0]):
				cursor.execute("SELECT qty FROM cust_ingredients WHERE cust_id={0} and ingr_id={1}".format(request.session['id'], abc[0]))
				quan = cursor.fetchone()
				if quan[0]!="":
					oqty = int(''.join(filter(str.isdigit, quan[0])))		
					qty += oqty
				print(oqty)
				
				print(qty)
				cursor.execute("call up_list_of_ingredient({0}, {1}, '{2}')".format(request.session['id'], abc[0], qty))
			else:
				cursor.execute("call list_of_ingredient({0}, {1}, '{2}')".format(request.session['id'], abc[0], qty))
			return render(request, 'pingredients.html', {'list_ingre':list_ingre})



def category(request, rec_name):
	print("in function")
	with connection.cursor() as cursor:
		cursor.execute("SELECT id FROM rec_categories WHERE name='{0}'".format(rec_name))
		id = cursor.fetchone()
		cursor.execute("SELECT name, directions FROM recipes WHERE category={0}".format(id[0]))
		recipes = cursor.fetchall()
		return render(request, 'events.html', {'recipes':recipes})


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
	if(email==""or passw==""):
		return render(request, 'index.html', {})
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
		return render(request, 'index.html', {})
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


def ingredients_present(user_ingredient_ids, matching_recipe_ids):
	dict = {}
	for i in range(user_ingredient_ids.__len__()):
		for temp in matching_recipe_ids[i]:
			keys = dict.setdefault(temp, [])	# adds key to dict & assigns a default value, if key not found in dict
			keys.append(user_ingredient_ids[i])
	return dict

#converts qty to an int & returns True if qty was in grams
def convert_qty(str):
	if str is None:
		return (0, True)	#does True or False, make a difference?
	elif str.strip()[-1:] == 'g':
		return (int(str.strip()[:-1]), True)
	else:
		return (int(str), False)
'''
#function to fetch recipe attributes like directions, if needed
def fetch_rec_directions(rec_id):
	cursor.execute("select directions from recipes where id = {0}".format(rec_id) )
	fetched = cursor.fetchone()
	if fetched is not None:
		return fetched[0]
	else:
		return fetched
'''
def fetch_unmatched_ingr_ids(rec_id, ingr_ids):
	query_str = "select ingr_id, qty from rec_ingredients where rec_id = {0}".format(rec_id)
	query_str2 = ""
	for ingr_id in ingr_ids:
		query_str2 += " and not ingr_id = {0}".format(ingr_id)
	#query_str2 = query_str2[:-4]	#removing the last " and"
	final_query_str = query_str + query_str2
	print("final_query_str = ", final_query_str)

	with connection.cursor() as cursor:
		cursor.execute(final_query_str)
		fetched = cursor.fetchall()
		if fetched is not None:
			return list(fetched)
		else:
			return fetched

def search_func(user_ingredients_with_qty):	#convert user qty to ints
	user_ingredients = list(user_ingredients_with_qty.keys())
	user_qty = list(user_ingredients_with_qty.values())

	error_message = ""

	#special case
	no_qty_specified = True
	for item in user_qty:
		if item is not None:
			no_qty_specified = False
			break

	# user_ingredients = ['potato', 'onion', 'flour']
	user_ingredient_ids = []
	user_ingredient_ids_with_qty = {}

	# converts ingredient name to ingredient_id in dictionary
	with connection.cursor() as cursor:
		for i in range(user_ingredients.__len__()):
			cursor.execute("select id from ingredients where name_english='{0}' or name_hindi='{1}'".format(user_ingredients[i], user_ingredients[i]))
			fetched = cursor.fetchone()
			if fetched is not None:
				ingredient_id = int(fetched[0])
				user_ingredient_ids_with_qty[ ingredient_id ] = user_qty[i]		#check
			else:
				err = "**ingredient id for '{0}' not found in db**".format(user_ingredients[i])
				error_message += err
				print(err)
				continue

	print("user_ingredient_ids_with_qty = ", user_ingredient_ids_with_qty)
	# user_ingredient_ids_with_qty =  {6: None, 7: None}

	user_ingredient_ids_with_qty_list = list(user_ingredient_ids_with_qty.items())
	print("user_ingredient_ids_with_qty_list = ", user_ingredient_ids_with_qty_list)
	# user_ingredient_ids_with_qty_list =  [(6, None), (7, None)]

	#user_ingr_qty_type = True #change

	matched_recipe_list = []
	#populating the list to be sorted
	with connection.cursor() as cursor:
		# fetching all recipes from db
		cursor.execute("select id from recipes")	#group by?
		fetched = cursor.fetchall()
		if fetched is not None:
			recipe_list = list(fetched)
			recipe_count = recipe_list.__len__()
		else:
			recipe_count = 0;
			err="**No recipes found in db**\n"
			error_message += err
			print(err)

		# recipe_list =  [(1,), (2,), (3,), (4,)]
		for i in range(recipe_list.__len__()):		#look for an alternative
			recipe_list[i] = recipe_list[i][0]
		print("recipe_list = ", recipe_list)
		# recipe_list =  [1, 2, 3, 4]

		current_index = 0
		# iterates through all recipes
		for i in range(recipe_count):
			rec_present_flag = False
			# checks if any user ingr is present in the recipe
			for j in range(user_ingredient_ids_with_qty_list.__len__()):
				user_ingr_id = user_ingredient_ids_with_qty_list[j][0]
				user_ingr_qty = user_ingredient_ids_with_qty_list[j][1]

				cursor.execute("select qty from rec_ingredients where rec_id={0} and ingr_id={1}".format(recipe_list[i], user_ingr_id))
				fetched = cursor.fetchone()
				if fetched is not None:
					(rec_ingr_qty, rec_ingr_qty_type) = convert_qty(fetched[0])
					(user_ingr_qty, user_ingr_qty_type) = convert_qty(user_ingr_qty)
					if(rec_ingr_qty_type == user_ingr_qty_type or no_qty_specified):
						if rec_ingr_qty > user_ingr_qty:
							subtracted_qty = rec_ingr_qty - user_ingr_qty
							if rec_ingr_qty_type:	#check if required
								subtracted_qty = str(subtracted_qty) + "g"
							else:
								subtracted_qty = str(subtracted_qty)
						else:
							subtracted_qty = None	#will not be rendered
					else:	#check
						subtracted_qty = "error"
						err="**grams cannot be compared with pieces**\n"
						error_message += err
						print(err)
						continue
					if not rec_present_flag:
						matched_recipe_list.append( [recipe_list[i]] )		#recipe id
						matched_recipe_list[current_index].append( [] )		#ingredients matched only by name not by qty
						matched_recipe_list[current_index].append( [] )		#ingredinets not matched by name
						matched_recipe_list[current_index].append( None )	#directions
						#matched_recipe_list[current_index].append(fetch_rec_directions(recipe_list[i]))
						rec_present_flag = True
						current_index += 1
					matched_recipe_list[current_index-1][1].append( (user_ingr_id, subtracted_qty) )
				else:
					pass	#print here will print redundant info, hence removed
			if rec_present_flag:
				for ret_tuple in fetch_unmatched_ingr_ids(recipe_list[i], list(user_ingredient_ids_with_qty.keys())):
					matched_recipe_list[current_index-1][2].append(ret_tuple)

	print("matched_recipe_list = ", matched_recipe_list)
	# matched_recipe_list =  [[3, [(6, '2'), (7, '150g')], [(4, None), (9, '75g'), (10, '15g'), (11, None), (12, '5g'), (13, None), (14, None)], None], [4, [(6, '1'), (7, '1')], [(15, '75g'), (16, '1g'), (17, '3g'), (18, '2g'), (19, None), (20, None), (4, None)], None]]


	#sorting the list
	sorted_list = sorted(matched_recipe_list, key=lambda elem: (-elem[1].__len__(), elem[2].__len__()))	#add condition to check missing quantites of ingredients
	#-ve value sorts in descending order

	print("sorted_list = ", sorted_list)
	# sorted_list =  [[3, [(6, '2'), (7, '150g')], [(4, None), (9, '75g'), (10, '15g'), (11, None), (12, '5g'), (13, None), (14, None)], None], [4, [(6, '1'), (7, '1')], [(15, '75g'), (16, '1g'), (17, '3g'), (18, '2g'), (19, None), (20, None), (4, None)], None]]

	#converting recipe ids & ingredient ids to names
	with connection.cursor() as cursor:
		for i in range(sorted_list.__len__()):
			rec_id = sorted_list[i][0]
			cursor.execute("select name, directions from recipes where id={0}".format(rec_id))
			fetched = cursor.fetchone()
			if fetched is not None and fetched[0] is not None:
				sorted_list[i][0] = fetched[0]
			else:
				err="**recipe name not found**\n"
				error_message += err
				print(err)
			
			#comment this to make sorted_list smaller to view
			'''
			if fetched is not None and fetched[1] is not None:
				sorted_list[i][3] = fetched[1]
			else:
				err="**recipe directions not found**\n"
				error_message += err
				print(err)
			'''

			for j in [1, 2]:
				for k in range(sorted_list[i][j].__len__()):	#case satisfied - ignores when sorted_list[i][j] is empty
					temp = sorted_list[i][j][k]
					temp_list = list(temp)		#check, is it better to change it to list at source
					ingr_id = temp[0]
					cursor.execute("select name_english from ingredients where id={0}".format(ingr_id))
					fetched = cursor.fetchone()
					#print("fetched = {0}, temp_list = {1}".format(fetched, temp_list))
					if fetched is not None:
						ingr_name = fetched[0]	#check, tupe or list, tuple looks better
						temp_list[0] = ingr_name
						sorted_list[i][j][k] = tuple(temp_list)
						#sorted_list[i][j][k][0] = ingr_name
					else:
						err="**name_english of ingredient not found**\n"
						error_message += err
						print(err)


	print("sorted_list = ", sorted_list)
	# sorted_list =  [['BHEL', [('potato', '2'), ('onion', '150g')], [('oil', None), ('coriander leaves', '75g'), ('cumin', '15g'), ('green chillies', None), ('black pepper', '5g'), ('tamarind', None), ('jaggery', None)], None], ['PAKORAS (SAVORY FRITTERS)', [('potato', '1'), ('onion', '1')], [(None, '75g'), ('red pepper', '1g'), ('salt', '3g'), (None, '2g'), ('paprika', None), ('spinach', None), ('oil', None)], None]]

	return (sorted_list, error_message)

@csrf_exempt
def search_for_recipes(request):
	
	#fetch posted data & convert it to a dictionary
	data = request.POST
	ingr_list = data.getlist('ingr[]')
	print("ingr_list from page = ", ingr_list)
	#ingr_list from page =  ['butter', 'cheese', 'potato', 'onion']
	user_ingredients_with_qty = {}
	for ingr in ingr_list:
		user_ingredients_with_qty.setdefault(ingr)

	print("user_ingredients_with_qty = ", user_ingredients_with_qty)
	#user_ingredients_with_qty = {'potato': 20, 'onion': 20, 'flour': 30}
	#user_ingredients_with_qty =  {'onion': None, 'potato': None, 'cheese': None, 'butter': None}


	(sorted_list, error_message) = search_func(user_ingredients_with_qty)


	#return HttpResponse(str(sorted_list)+'<br><br>'+error_message)
	return render(request, 'blog.html', {"sorted_list": sorted_list, "error_message": error_message, "qty_specified": False, "limit":3})

def customers(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT name FROM customers")
		row = cursor.fetchone()
	return HttpResponse(row)


def contact(request):
	return render(request, 'contact.html', {})
