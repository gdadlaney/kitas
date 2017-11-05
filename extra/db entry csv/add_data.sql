

-- run -> mysql -u root -p kitas < add_data.sql 

\W	-- show warnings enabled --

-- deleting previous data --

delete from cust_activity;
delete from cust_fav;
delete from cust_ingredients;
delete from rec_ingredients;
delete from ingredients;
delete from recipes;
delete from ingr_categories;
delete from rec_categories;
delete from customers;

load data local infile "customers.csv"
into table customers
fields terminated by "\t"
LINES TERMINATED BY '\n'
ignore 1 lines;

load data local infile "rec_categories.csv"
into table rec_categories
fields terminated by "\t"
LINES TERMINATED BY '\n'
ignore 1 lines
(id, name, @my_description)
SET
description = nullif(@my_description, 'NULL');

load data local infile "ingr_categories.csv"
into table ingr_categories
fields terminated by "\t"
LINES TERMINATED BY '\n'
ignore 1 lines;

load data local infile "recipes.csv"
into table recipes
fields terminated by "\t"
LINES TERMINATED BY '\n'
ignore 1 lines
(id, name, directions, cust_id, @my_time_modified, @my_servings, @my_prep_time, category)
SET
time_modified = nullif(@my_time_modified, 'NULL'),
servings = nullif(@my_servings, 'NULL'),
prep_time = nullif(@my_prep_time, 'NULL');

load data local infile "ingredients.csv"
into table ingredients
fields terminated by "\t"
LINES TERMINATED BY '\n'
ignore 1 lines
(id, @my_name_english, @my_name_hindi, category)
SET
name_english = nullif(@my_name_english, 'NULL'),
name_hindi = nullif(@my_name_hindi, 'NULL');

load data local infile "rec_ingredients.csv"
into table rec_ingredients
fields terminated by "\t"
LINES TERMINATED BY '\n'
ignore 1 lines
(rec_id, @my_qty_string, ingr_string, @my_qty, @my_ingr_id)
SET
qty_string = nullif(@my_qty_string, 'NULL'),
qty = nullif(@my_qty, 'NULL'),
ingr_id = nullif(@my_ingr_id, 'NULL');

-- load data local infile "cust_ingredients.csv"
-- into table cust_ingredients
-- fields terminated by "\t"
-- LINES TERMINATED BY '\n'
-- ignore 1 lines
-- (cust_id, ingr_id, @my_qty)
-- SET
-- qty = nullif(@my_qty, 'NULL');


\w	-- show warnings disabled --
