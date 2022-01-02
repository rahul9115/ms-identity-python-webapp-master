import random
import string
import os
import random_address
import names
from datetime import datetime, timedelta
import sqlite3
from operations import fetch_data, add_new_user, conn

def generate_users_file(file_name, no_of_users=100):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'a') as f:
        for i in range(1,no_of_users+1):
            emp_id = str(1000+i)
            first_name, last_name = names.get_full_name().split()
            designation = random.choice(['P1', 'P2', 'P3', 'P4'])
            email = first_name+last_name+''.join(random.choices(string.digits,k=4))+'@'+'lntinfotech.com'
            mobile = random.choice(['9','8','7'])+''.join(random.choices(string.digits,k=9))
            random_addresss = random_address.real_random_address()
            a = []
            if 'address1' in random_addresss:
                a.append(random_addresss['address1'])
            if 'city' in random_addresss:
                a.append(random_addresss['city'])
            if 'state' in random_addresss:
                a.append(random_addresss['state'])
            address = ' '.join(a)
            
            is_enabled = "True"
            is_admin = "False"
            
            final_string = f"{emp_id},{first_name},{last_name},{designation},{email},{mobile},{address},{is_enabled},{is_admin}"
            f.write(final_string)
            f.write('\n')

def add_admin():
	emp_id = '1000'
	first_name = 'Admin'
	last_name = 'TheGreat'
	designation = 'P4'
	email = first_name+last_name+'1000@lntinfotech.com'
	mobile = random.choice(['9','8','7'])+''.join(random.choices(string.digits,k=9))
	random_addresss = random_address.real_random_address()
	a = []
	if 'address1' in random_addresss:
		a.append(random_addresss['address1'])
	if 'city' in random_addresss:
		a.append(random_addresss['city'])
	if 'state' in random_addresss:
		a.append(random_addresss['state'])
	address = ' '.join(a)

	is_enabled = "True"
	is_admin = "True"
	pass_id = '0'
	user_details = [emp_id,first_name,last_name,designation,email,mobile,address,is_enabled,is_admin,pass_id]

	password = 'Password1'
	creation_date = '01/01/2000'
	expiry_date = '31/12/2099'
	password_history = 'AdminRocks1000'
	password_details = [pass_id, password, creation_date, expiry_date, password_history]

	conn = sqlite3.connect('database.db')
	cur = conn.cursor()
	query1 = "insert into Employee values ("+"?,"*(len(user_details)-1)+"?)"
	cur.execute(query1, user_details)
	query2 = "insert into Password values(?,?,?,?,?)"
	cur.execute(query2, password_details)
	conn.commit()

def read_from_file(file, password_timestamp=60):
    total = len(fetch_data(conn, "Employee", '*'))
    with open(file, 'r') as f:
        itemset = f.readlines()
        for i,item in enumerate(itemset):
            user_details = item.split(',')
            user_details = list(user_details)
            for i in range(len(user_details)):
                if user_details[i] == "":
                    user_details[i] = "NA"
            
            pass_id = total+i
            password = 'Newpassword123'
            today = datetime.today()
            creation_date = str(today).split()[0]
            expiry_date = str(today+timedelta(days=password_timestamp)).split()[0]
            
            password_details = [pass_id, password, creation_date, expiry_date]
            user_details.append(pass_id)
            add_new_user(conn, user_details, password_details)
            
            
file_name = "users_file.csv"

generate_users_file(file_name, no_of_users=100)
add_admin()
read_from_file(file_name)
