import sqlite3
import smtplib, ssl
from queries import *
from sqlite3 import Error
from datetime import datetime, timedelta

conn = sqlite3.connect("database.db")

def create_table(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
    except Error as e:
        print(e)

# Tables creation
create_table(create_employees_table)
create_table(create_group_table)
create_table(create_password_table)


def add_new_user(conn, user_details, password_details):   
    cur = conn.cursor()
    
    if isinstance(user_details, list):    
        query1 = "insert into Employee values ("+"?,"*(len(user_details)-1)+"?)"
        cur.execute(query1, user_details)
        
    if isinstance(password_details, list):
        password_details.append(password_details[1])
        query2 = "insert into Password values(?,?,?,?,?)"
        cur.execute(query2, password_details)
    
    conn.commit()

def fetch_data(conn, table, columns):
    if isinstance(columns, list):
        columns = ','.join(columns)
    query = "select "+columns+" from "+table
    cur = conn.cursor()
    a = cur.execute(query)
    result = []
    for i in a:
        result.append(i)
    conn.commit()
    return result
        
def create_group(conn, group_name, group_desc="No Description Available"):
    cur = conn.cursor()
    result = fetch_data(conn, "Group_table","*")
    all_group_names = []
    if len(result)>1:
        all_group_names = [i[1].lower() for i in result]
    
    if group_name.lower() in all_group_names:
        print("Group name already taken.")
        return
    
    total = len(result)
    query = "insert into Group_table values(?,?,?)"
    cur.execute(query, (total+1, group_name, group_desc))
    conn.commit()

# for data in group_data:
#     create_group(conn, data[0], data[1])
    
def create_admin_group_mapping(emp_id, group_id):
    cur = conn.cursor()
    query = "insert into Admin_group_map values(?,?)"
    cur.execute(query, (emp_id, group_id))
    conn.commit()
    



        
        
        
def reset_password(conn, emp_id, password):
    cur = conn.cursor()
    query1 = "select pass_id from Employee where emp_id = "+str(emp_id)
    
    pass_id = list(cur.execute(query1))[0][0]
    
    query2 = """update Password 
        set password = '{}' 
        where pass_id= '{}'
    """.format(password, pass_id)
    
    cur.execute(query2)
    conn.commit()
    

def enable_or_disable_user(conn, emp_id, action):
    cur = conn.cursor()
    query1 = "select is_enabled from Employee where emp_id = {}".format(emp_id)
    is_enabled = list(cur.execute(query1))[0][0]
    
    if action == 'enable':
        if is_enabled == 'False':
            query2 = """update Employee 
                set is_enabled = 'True' 
                where emp_id= '{}'
            """.format(emp_id)
            
            cur.execute(query2)
        else:
            print("Employee already enabled")
            
    elif action == 'disable':
        if is_enabled == 'True':
            query3 = """update Employee 
                set is_enabled = 'False'
                where emp_id= '{}'
            """.format(emp_id)
            
            cur.execute(query3)
        else:
            print("Employee already disabled")
    
    else:
        print("Wrong action specified. I couldn't unserstand.")
    conn.commit()
        
    
def delete_employee(conn, emp_id):
    cur = conn.cursor()
    
    query0 = "select pass_id from Employee where emp_id = {}".format(emp_id)
    pass_id = list(cur.execute(query0))[0][0]
    
    query1 = "delete from Employee where emp_id = {}".format(emp_id)
    cur.execute(query1)
    
    query2 = "delete from Password where pass_id = {}".format(pass_id)
    cur.execute(query2)
    conn.commit()
    

def promote_employee(conn, emp_id, val=1):
    cur = conn.cursor()
    designations = ['P1','P2','P3','P4', 'P5', 'P6']
    query0 = "select designation from Employee where emp_id = {}".format(emp_id)
    designation = list(cur.execute(query0))[0][0]
    
    index = designations.index(designation)
    if index == 3:
        print("Employee cannot be promoted anymore.")
        return
    
    query1 = """
        update Employee
        set designation = "{}"
        where emp_id = {}
    """.format(designations[index+val], emp_id)
    
    cur.execute(query1)
    
    conn.commit()
        
        

def send_msg(sender, receiver, password):
    port = 465
    smtp_mail = "smtp.gmail.com"
    
    # sender = "testmailforpython1068@gmail.com"
    # receiver = "testmailforpython1068@gmail.com"
    # password = '10689218chai'
    
    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test
    
    This is a test e-mail message.
    """
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_mail, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
        





# fetch_data(conn, "Employee", "*")
# fetch_data(conn, "Password", "*")
# fetch_data(conn, "Group_table", "*")

# create_group(conn, "Group1", "*")
    

# user_details = [(105,"employee105","abc","def","P2","abc@d.com","2","999","abcd",7,"True", "False")]
# password_details = [(7,"ab12",'31/12/2099')]

# add_new_user(conn, user_details, password_details)


# reset_password(conn, 2, "Brbc")

# enable_or_disable_user(conn, 1, action='enable')

# delete_employee(conn, 7)

# promote_employee(conn, 2)


# def check_admin(email):
#     result = fetch_data(conn, "Employee", "is_admin")[0]
#     return True if result == "True" else False

    
