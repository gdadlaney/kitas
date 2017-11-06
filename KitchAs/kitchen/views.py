import json
from django.shortcuts import render, redirect
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


def favrecipe(request):
	print(request.POST.get('name'))
	return render(request, 'index.html', {})

def categories(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT name, description FROM rec_categories LIMIT 6")
		rec_category = list(cursor.fetchall())
		for i in range(rec_category.__len__()):
			rec_category[i] = list(rec_category[i])
	return render(request, 'categories.html', {'rec_category':rec_category})

def SearchFromPantry(request):
	if request.session['user']==None:
		return redirect('/index')
	request.session['search_from_pantry'] = True
	return redirect('/ingredients')

def SearchFromCheckboxes(request):
	request.session['search_from_pantry'] = False
	return redirect('/ingredients')

def ingredients(request):
	#user is logged in
	if request.session.get("search_from_pantry") == True :
		show_checkboxes = False
		with connection.cursor() as cursor:
			cursor.execute("SELECT ingr_id, qty FROM cust_ingredients where cust_id={0}".format(request.session['id']))
			fetched = cursor.fetchall()		#fetchone or fetchall doesn't matter
			if fetched is None:
				show_checkboxes = True
	else:
		show_checkboxes = True


	if not show_checkboxes:
		return redirect('/search_result')
	else:
		with connection.cursor() as cursor:
			cursor.execute("SELECT id, name FROM ingr_categories")
			rec_category = list(cursor.fetchall())	#checking condition
			ingr_categories = []
			for i in range(rec_category.__len__()):
				ingr_cat_id = rec_category[i][0]
				ingr_cat_name = rec_category[i][1]
				cursor.execute("SELECT name_english FROM ingredients where category={0} ORDER BY name_english".format(ingr_cat_id))
				fetched = cursor.fetchall()
				if fetched == ():
					continue
				ingr_names = list(fetched)
				for j in range(ingr_names.__len__()):
					ingr_names[j] = ingr_names[j][0]
				ingr_categories.append([ingr_cat_name, ingr_names])

			collapse = []
			for i in range(ingr_categories.__len__()):
				collapse.append("collapse"+str(i+1))

		print("ingr_categories = ", ingr_categories)
		#ingr_categories =  [['Vegetables', ['Chick peas', 'coriander leaves', 'onion', 'potato', 'spinach', 'tomato']], ['Grains', ['Chickpea flour', 'flour', 'wheat flour']], ['Spices', ['black pepper', 'Cardamom', 'Cinnamon stick', 'Coconut powder', 'Coriander powder', 'cumin', 'Cumin seeds', 'Garam Masala', 'Garlic', 'Ginger powder', 'green chillies', 'Hot pepper', 'jaggery', 'Mango powder', 'Mustard seeds', 'paprika', 'poppy seeds', 'red pepper', 'salt', 'tamarind', 'Turmeric powder']], ['Others', ['ghee', 'oil', 'puffed rice']]]
		print("collapse = ", collapse)
		#collapse =  ['collapse1', 'collapse2', 'collapse3', 'collapse4']

		ingr_categories_with_extras = list(zip(ingr_categories, collapse))
		print("ingr_categories_with_extras = ", ingr_categories_with_extras)
		#ingr_categories_with_extras =  [(['Vegetables', ['Chick peas', 'coriander leaves', 'onion', 'potato', 'spinach', 'tomato']], 'collapse1'), (['Grains', ['Chickpea flour', 'flour', 'wheat flour']], 'collapse2'), (['Spices', ['black pepper', 'Cardamom', 'Cinnamon stick', 'Coconut powder', 'Coriander powder', 'cumin', 'Cumin seeds', 'Garam Masala', 'Garlic', 'Ginger powder', 'green chillies', 'Hot pepper', 'jaggery', 'Mango powder', 'Mustard seeds', 'paprika', 'poppy seeds', 'red pepper', 'salt', 'tamarind', 'Turmeric powder']], 'collapse3'), (['Others', ['ghee', 'oil', 'puffed rice']], 'collapse4')]

		return render(request, 'ingredients.html', {"ingr_categories_with_extras":ingr_categories_with_extras})



def myrecipe(request):
	if request.session['user']=="admin":
		with connection.cursor() as cursor:
			cursor.execute("SELECT name, directions FROM recipes")
			usr_recipes = cursor.fetchall()
		return render(request, 'myrecipe.html', {'usr_recipes':usr_recipes})
	elif request.session['user'] != None:
		with connection.cursor() as cursor:
			cursor.execute("SELECT name, directions FROM recipes WHERE cust_id={0}".format(request.session['id']))
			usr_recipes = cursor.fetchall()
		return render(request, 'myrecipe.html', {'usr_recipes':usr_recipes})
	else:
		return render(request, 'index.html', {})


def accounts(request):
	return render(request, 'index.html/#cd-login', {"ingr_categories": ingr_categories})


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
			cursor.execute("INSERT INTO cust_activity (cust_id,rec_id) values ({0},{1})".format(request.session['id'],rec_id))
			cursor.execute("SELECT ingr_id, qty FROM rec_ingredients WHERE rec_id={0}".format(rec_id))
			list_ingre_w_qty = cursor.fetchall()
			
			for i in range(data_list.__len__()):
				for j in range(list_ingre_w_qty.__len__()):
					if data_list[i][0]==list_ingre_w_qty[j][0]:
						qt1 = convert_qty( data_list[i][1])
						qt2 = convert_qty( list_ingre_w_qty[j][1])

						if(list_ingre_w_qty[j][1]!=None and qt1[1]==qt2[1]):
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
		recipe_info = list(cursor.fetchone())
		print("Recipe basic info = ", recipe_info)

		sorted_list = request.session.get('sorted_list')
		error_message = request.session.get('error_message')
		#print("sorted_list = ", sorted_list)
		if error_message is not None:
			print("error_message = ", error_message)

		# making space for ingredients matching & missing lists
		recipe_info.append(recipe_info[1])
		recipe_info.append(recipe_info[2])

		for temp in sorted_list:
			if recipe_info[0] == temp[0]:
				recipe_info[1] = temp[1]
				recipe_info[2] = temp[2]
			else:
				print("No matching recipe name in DB")

		print("Final recipe_info = ", recipe_info)

	return render(request, 'single.html', {'recipe_info':recipe_info})


def single2(request, rec_name):
	with connection.cursor() as cursor:
		cursor.execute("SELECT name, directions, time_modified, id FROM recipes where name='{0}'".format(rec_name))
		recipe_info = list(cursor.fetchone())
		print("\n Recipe basic info = ", recipe_info)

		recipe_id = recipe_info[3]
		recipe_info.pop()		#recipe id not needed further

		cursor.execute("SELECT name_english, qty_string, ingr_string FROM rec_ingredients, ingredients where rec_ingredients.ingr_id=ingredients.id and rec_ingredients.rec_id='{0}'".format(recipe_id))
		recipe_str = list(cursor.fetchall())
		print("\n Recipe user display string = ", recipe_str)

		sorted_list_copy = request.session.get('sorted_list_copy')
		error_message = request.session.get('error_message')
		print("\n sorted_list_copy = ", sorted_list_copy)
		if error_message is not None:
			print("\n error_message = ", error_message)

		# making space for ingredients matching & missing lists
		#recipe_info.append(recipe_info[1])
		#recipe_info.append(recipe_info[2])

		for temp in sorted_list_copy:
			if recipe_info[0] == temp[0]:
				recipe_info.insert(1, temp[1])
				recipe_info.insert(2, temp[2])
			else:
				print("**No matching recipe name in DB**")

		print("\n Intermediate recipe_info = ", recipe_info)


		for i in [1, 2]:
			for j in range(len(recipe_info[i])):
				flag = False
				for temp in recipe_str:
					if temp[0] == recipe_info[i][j][0]:
						flag = True
						recipe_info[i][j].insert(0, temp[1])
						recipe_info[i][j].insert(1, temp[2])
				if flag is False:
					print("**Error in last part of 'single2'**")

		print("\n Final recipe_info = ", recipe_info)
		# Final recipe_info =  ['BHEL', [['1 packet', 'Bhel mix or Sev', 'puffed rice', None]], [['2', 'Mashed boiled potatoes (mashed coarsely and then salted)', 'potato', '2'], ['1/2 cup', 'Chopped fresh coriander leaves (a.k.a Chinese parsley)', 'coriander leaves', '75g'], ['3 tsp', 'Freshly roasted and ground cumin', 'cumin', '15g'], ['to taste', 'Green chilies', 'green chillies', None], ['1-2 tsp', 'Freshly ground black pepper', 'black pepper', '5g'], ['to taste', 'Tamarind', 'tamarind', None], ['to taste', 'Jaggery (or Brown Sugar)', 'jaggery', None], ['1 cup', 'Chopped onions.', 'onion', '150g']], 'First boil the potatoes, mash them, salt them, and add pepper to taste. Add some coriander leaves too. <br><br>Roast the cumin and grind it.<br><br>Dissolve about 4 Tbsp of tamarind concentrate in 1 cup of hot water, and let it simmer and thicken gradually. Dissolve the jaggery (or sugar) until the sauce becomes tart and slightly sweet. (You may add some salt<br>and ground red paprika, if you want to.) The sauce should be of a consistency slightly thinner than maple syrup. Pour into a serving container (like a creamer). Mix the puffed rice and sev/bhel mix in a large bowl. <br><br>On a plate, serve the rice-bhel mixture, add the potatoes, then the onions, chilies, and then dust the cumin powder over it. Next pour on the sauce and top with the coriander garnish. (Add salt/pepper to<br>taste). <br><br>Mix the ingredients on the plate and eat. <br>', datetime.datetime(2017, 11, 5, 16, 23, 59)]

	return render(request, 'single2.html', {'recipe_info':recipe_info})


#add user recipes
@csrf_protect
def subRecipe(request):
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		data = request.POST
		name = (data.get('name')).upper()
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
		return render(request, 'index.html', {"alert_message": "Looks like you haven't logged in"})
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

	request.session['search_from_pantry'] = True	#required for search by ingredients

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
		return render(request, "index.html", {})

def logout(request):
	if request.session['user'] != None:
		user = request.session['user']
	else:
		user = " "
	request.session['user']=None
	request.session['id']=None

	request.session['search_from_pantry']=False

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

def search_func(user_ingredient_ids_with_qty):	#convert user qty to ints
	user_ingredient_ids = list(user_ingredient_ids_with_qty.keys())
	user_qty = list(user_ingredient_ids_with_qty.values())

	error_message = ""

	#special case
	no_qty_specified = True
	for item in user_qty:
		if item is not None:
			no_qty_specified = False
			break

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
						matched_recipe_list[current_index].append( [] )		#ingredients not matched by name
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
			
			# ******* comment this to make sorted_list smaller to view ***********
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

def ShortenIngredientList(sorted_list, count):

	short_list = sorted_list

	for i in range(len(sorted_list)):
		cnt = count
		if( len(sorted_list[i][1]) >= cnt ):
			short_list[i][1] = sorted_list[i][1][:cnt]
			short_list[i][2] = []
		else:
			cnt -= len(sorted_list[i][1])
			short_list[i][2] = sorted_list[i][2][:cnt]

	print("Shortened List = ", short_list)

	return short_list

@csrf_exempt
def search_result(request):

	user_ingredient_ids_with_qty = {}

	if request.session.get("search_from_pantry") == True:
		ingrs_from_checkboxes = False
		with connection.cursor() as cursor:
			cursor.execute("SELECT ingr_id, qty FROM cust_ingredients where cust_id={0}".format(request.session['id']))
			fetched = cursor.fetchall()
			# no need to check this, already checked in /ingredients
			if fetched is None:
				ingrs_from_checkboxes = True
				#break #doesn't work, not needed anyway
			else:
				pantry_ingrs = list(fetched)
				for pantry_ingr in pantry_ingrs:
					ingr_id = pantry_ingr[0]
					qty = pantry_ingr[1]
					user_ingredient_ids_with_qty[ingr_id] = qty

			print("user_ingredient_ids_with_qty = ", user_ingredient_ids_with_qty)
			#

	else:
		ingrs_from_checkboxes = True

	# using pantry
	if not ingrs_from_checkboxes:
		(sorted_list, error_message) = search_func(user_ingredient_ids_with_qty)

		request.session['sorted_list'] = sorted_list[:]	#a reference would change, hence a copy ( performance penalty? )
		request.session['error_message'] = error_message

		sorted_list = ShortenIngredientList(sorted_list, 5)

		#return HttpResponse(str(sorted_list)+'<br><br>'+error_message)
		return render(request, 'search_result.html', {"sorted_list": sorted_list, "error_message": error_message, "qty_specified": True,"message1": "From your pantry", "message2": "To manually select ingredient to make a recipe, click ", "link1": "/SearchFromCheckboxes"})
	else:
		#fetch posted data & convert it to a dictionary
		data = request.POST
		ingr_list = data.getlist('ingr[]')
		print("ingr_list from page = ", ingr_list)
		#ingr_list from page =  ['butter', 'cheese', 'potato', 'onion']
		
		ingr_id_list = []
		with connection.cursor() as cursor:
			for ingr_name in ingr_list:
				cursor.execute("SELECT id FROM ingredients where name_english='{0}' or name_hindi='{0}'".format(ingr_name))
				fetched = cursor.fetchone()
				if fetched is None:
					print("**No match found for the ingredient '{0}' in db**".format(ingr_name))
				else:
					ingr_id_list.append(fetched[0])

		for ingr_id in ingr_id_list:
			user_ingredient_ids_with_qty.setdefault(ingr_id)

		print("user_ingredient_ids_with_qty = ", user_ingredient_ids_with_qty)
		#

		(sorted_list, error_message) = search_func(user_ingredient_ids_with_qty)

		request.session['sorted_list'] = sorted_list[:]	#a reference would change, hence a copy ( performance penalty? )
		request.session['error_message'] = error_message

		sorted_list = ShortenIngredientList(sorted_list, 5)

		#return HttpResponse(str(sorted_list)+'<br><br>'+error_message)
		return render(request, 'search_result.html', {"sorted_list": sorted_list, "error_message": error_message, "qty_specified": False, "message1":"From selected ingredients", "message2": "You can also search using ingredients of your pantry, click ", "link1": "/SearchFromPantry"})

def customers(request):
	with connection.cursor() as cursor:
		cursor.execute("SELECT name FROM customers")
		row = cursor.fetchone()
	return HttpResponse(row)


def contact(request):
	return render(request, 'contact.html', {})


def delRecipeUser(request, rec_name):
	if request.session['user']==None:
		return render(request, 'index.html', {})
	else:
		userid = request.session['id']
		with connection.cursor() as cursor:
			cursor.execute("SELECT id FROM recipes where name='{0}'".format(rec_name))
			recid=cursor.fetchone()
			cursor.execute("DELETE from rec_ingredients where rec_id={0}".format(recid[0]))
			cursor.execute("DELETE from recipes where id={0}".format(recid[0]))
			cursor.execute("SELECT name, directions FROM recipes WHERE cust_id={0}".format(request.session['id']))
			usr_recipes = cursor.fetchall()
			return render(request, 'myrecipe.html', {'usr_recipes':usr_recipes})

@csrf_protect
def delRecipe(request):
	if request.session['user'] == "admin":
		recname = (request.POST.get("recname")).upper()
		print(recname)		
		with connection.cursor() as cursor:
			cursor.execute("SELECT id FROM recipes where name='{0}' ".format(recname))
			recid=cursor.fetchone()
			cursor.execute("DELETE from rec_ingredients where rec_id={0}".format(recid[0]))
			cursor.execute("DELETE from recipes where id={0}".format(recid[0]))
			return render(request, 'admin.html', {})
	else:
		return render(request, "index.html", {})
	



def admin(request):
	if request.session['user'] == "admin":
		return render(request, 'admin.html', {})
	else:
		return render(request, "index.html", {})
