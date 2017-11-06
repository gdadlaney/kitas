\d //

create procedure list_of_ingredient(in uid int, in iid int, in quantity varchar(20)) begin insert into cust_ingredients values(uid, iid, quantity) ; end //

create procedure up_list_of_ingredient(in uid int, in iid int, in quantity varchar(20)) begin update cust_ingredients set qty=quantity where cust_id=uid and ingr_id=iid ; end //

\d ;
