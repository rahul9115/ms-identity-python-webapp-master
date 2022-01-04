import uuid
import re
import requests
import smtplib, ssl
from flask import Flask, render_template, session, request, redirect, url_for,flash
import flask
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config
import sqlite3
from flask_mail import Mail, Message
con=sqlite3.connect("database.db")
reg=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def send_msg(receiver):
    port = 465
    smtp_mail = "smtp.gmail.com"
    print("receive",receiver)
    sender = "team6bot@gmail.com"
    # receiver = "testmailforpython1068@gmail.com"
    password = 'Chaitanya@10685227'
    
    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test
    
    This is a test e-mail message.
    """
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_mail, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)
app.config['SECRET_KEY'] = 'stadium'
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='bot091281@gmail.com' #input mail
app.config['MAIL_PASSWORD']='Manoj@123' #change this before pushing to git
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True


# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
username=""
@app.route("/")
def index():
    session["admin"]=[True]
    if not session.get("user") or session["admin"][0]==[False]:
       session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
       return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        print("session_details",session["user"])
        username=session["user"].get('preferred_username')
        print("username",username)
        con = sqlite3.connect("database.db")
        cur=con.cursor()
        session["admin"]=[False]
        enabled=True
        admin=False
        values=cur.execute(f"select is_enabled,is_admin from Employee where email='{username}'")
        for i in values:
            print("this",i[0])
            enabled=i[0]
            admin=i[1]
        con.close()
        name=session["user"].get("name")
        print("why",enabled,admin)
        if(enabled=="True" and admin=="True"):
            print("inside very")
            session['admin'][0]=True
            
            return render_template("after.html", user=(name.split(" "))[0], version=msal.__version__)
        elif(enabled=="True"):
            session["admin"][0]=False
            return redirect(url_for("employee"))
        else:
            session["users"]=[]
            session.clear() # Wipe out user and its token cache from session
            print("This",url_for("index",_external=True))
            return redirect(url_for("index"))
@app.route("/request1")
def request1():
    if not session.get("user") or session["admin"]==True:
       session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
       return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        return render_template("raise_colab.html")
@app.route("/raise1",methods=["POST","GET"])
def raise1():
    if request.method=="POST":
        if not session.get("user") or session["admin"]==True:
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
        else:
            username=session["user"].get('preferred_username')
            con = sqlite3.connect("database.db")
            cur=con.cursor()
            session["admin"]=[False]
            enabled=True
            admin=False
            values=cur.execute(f"select emp_id from Employee where email='{username}'")
            emp_id=0
            for i in values:
                emp_id=i[0]
                
            con.close()
            con = sqlite3.connect("database.db")
            cur=con.cursor()
            
            values=cur.execute(f"select email from Employee where is_admin='True'")
            email=0
            for i in values:
                print("this",i)
                email=i[0]
                
            con.close()
            subject=request.form.get("subject")
            description=request.form.get("issue")
            print("cred",email,subject,description,emp_id)
            with app.app_context():
                message = f"""

                Subject: {subject}
                Description: {description}
                Request raised by folowing: 
                Emp_Id:{emp_id}
                """
                mail=Mail(app)
                sender = 'bot091281@gmail.com'
                #receiver = 'bot091281@gmail.com'
                msg = Message(subject='SMTP e-mail test',sender=sender,recipients=[email])
                msg.body = str(message)
                mail.send(msg)
            return render_template("raise_colab.html")
@app.route("/search")
def employee():
    
    if not session.get("user"):
       session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
       return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        if session["admin"][0]==True:
            file_name=""
            conn = sqlite3.connect("database.db")
            name=session["user"].get("name")
            cur = conn.cursor()
            username=session["user"].get('preferred_username')
            values=cur.execute(f"select * from employee where email='{username}'")
            print("user",username)
            data={}
            for i in values:
                print(i)
                data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}
                file_name=i[10]
            print("data",data)
            name=session["user"].get("name")
            conn.close()
            conn = sqlite3.connect("database.db")
            name=session["user"].get("name")
            cur = conn.cursor()
            username=session["user"].get('preferred_username')
            values=cur.execute(f"select group_id from employee_group_map where emp_id='{data.get('EMP_ID')}'")
            group_names=[]
            for i in values:
                print(i)

                conn = sqlite3.connect("database.db")
                name=session["user"].get("name")
                cur = conn.cursor()
                value1=cur.execute(f"select group_name from group_table where group_id='{i[0]}'")
                for j in value1:
                    group_names.append(j[0])


            return render_template("admin_colab.html", user=(name.split(" "))[0],list=data,group_names=group_names,file_name=file_name, version=msal.__version__)
        elif session["admin"][0]==False:
            file_name=""
            conn = sqlite3.connect("database.db")
            name=session["user"].get("name")
            cur = conn.cursor()
            username=session["user"].get('preferred_username')
            values=cur.execute(f"select * from employee where email='{username}'")
            data={}
            
            for i in values:
                data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}
                file_name=i[10]
            print("yo",file_name)
            name=session["user"].get("name")
            conn.close()
            conn = sqlite3.connect("database.db")
            name=session["user"].get("name")
            cur = conn.cursor()
            username=session["user"].get('preferred_username')
            values=cur.execute(f"select group_id from employee_group_map where emp_id='{data.get('EMP_ID')}'")
            group_names=[]
            for i in values:
                print(i)

                conn = sqlite3.connect("database.db")
                name=session["user"].get("name")
                cur = conn.cursor()
                value1=cur.execute(f"select group_name from group_table where group_id='{i[0]}'")
                for j in value1:
                    group_names.append(j[0])
                conn.close()
            print(group_names)
            conn.close()
            str1="{"+f"{{ url_for('static',filename='/img/{file_name}') }}"+"}"
            print(str1)
            return render_template("employee_colab.html", user=(name.split(" "))[0],list=data,group_names=group_names,file_name=file_name, version=msal.__version__)

@app.route("/search")
def search():
    if not session.get("user") or session["admin"][0]==False:
       session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
       return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    

    name=session["user"].get("name")
    
    return render_template("search_colab.html", user=(name.split(" "))[0], version=msal.__version__)
@app.route("/crud",methods=["POST","GET"])
def crud():
    if request.method=="POST":
        print("in")
        if not session.get("user") or session["admin"][0]==False:
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
            
            
        else:
            
            conn = sqlite3.connect("database.db")
            
            emp_id=request.form.get("Emp_ID")
            fname=request.form.get("fname")
            lname=request.form.get("lname")
            desig=request.form.get("desig")
            email=request.form.get("email")
            mobile=request.form.get("mobile")
            address=request.form.get("address")
            gender=request.form.get("gender")
            is_admin=request.form.get("admin")
            enabled=request.form.get("enabled")
            image=request.files["image"]
            name=session["user"].get("name")
            b_email=True
            b_number=True
            b_emp_id=True

            if(len(str(mobile))!=10):
                b_email=False
                
                
                
            if(re.fullmatch(reg,email) is None):
                b_number=False
            
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            values=cur.execute("select * from employee")
            list1=[]
            list1=[]
            for i in values:
                data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}
                list1.append(data)
            conn.close()
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            values=cur.execute("select emp_id from employee")
            for i in values:
                if(int(i[0])==int(emp_id)):
                    print("emp_value",i[0])
                    conn.close()
                    return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible",mv="hidden",me="visible",mobile_message="",email_message="",emp="visible",emp_message="duplicate emp_id")
            conn.close()
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            values=cur.execute("select email from employee")
            for i in values:
                if(i[0]==email):
                    print("emp_value",i[0])
                    conn.close()
                    return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible",mv="hidden",me="visible",mobile_message="",email_message="",emp="",emp_message="",em="visible",email_message1="Duplicate email")        


           

            if(b_email==False and b_number==False):
                return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible",mv="visible",me="visible",mobile_message="Please enter 10 digit mobile number",email_message="Please enter valid email",emp="hidden",emp_message="",em="hidden",email_message1="")
            elif b_number==False:
                return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible",mv="visble",me="hidden",mobile_message="Please enter 10 digit mobile number",email_message="",emp="hidden",emp_message="",em="hidden",email_message1="")
            elif b_email==False:
                return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible",mv="hidden",me="visible",mobile_message="",email_message="Please enter valid email",emp="hidden",emp_message="",em="hidden",email_message1="")



            
            image.save(f"C:/Users/sudha/Downloads/ms-identity-python-webapp-master/static/img/{image.filename}") 
            print("image",image)
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            cur.execute(f"INSERT INTO Employee VALUES({emp_id},'{fname}','{lname}','{desig}','{email}',{mobile},'{address}','{enabled}','{is_admin}',1,'{image.filename}','{gender}')")
            conn.commit()
            conn.close()
            
            print("Executed")
            print(email)
            with app.app_context():
                message = "Admin has inserted your data."
                mail=Mail(app)
                sender = 'bot091281@gmail.com'
                #receiver = 'bot091281@gmail.com'
                msg = Message(subject='SMTP e-mail test',sender=sender,recipients=[email])
                msg.body = str(message)
                mail.send(msg)
            #send_msg(email)
            return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible",mv="hidden",me="visible",mobile_message="",email_message="",emp="hidden",emp_message="",em="hidden",email_message1="")
            
    else:   
        if not session.get("user") or session["admin"][0]==False:
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
        else:
            print("good work")
            name=session["user"].get("name")
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            values=cur.execute("select * from employee")
            list1=[]
            for i in values:
                data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}
                list1.append(data)
            print(list1)
            conn.close()
        return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible",mv="hidden",me="visible",mobile_message="",email_message="",emp="hidden",emp_message="",em="hidden",email_message1="")
            
@app.route("/group",methods=["POST","GET"])
def group():
    if request.method=="POST":
        print("in")
        if not session.get("user") or session["admin"][0]==False:
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
            
            
        else:
            
            conn = sqlite3.connect("database.db")
            
            emp_id=request.form.get("Emp_ID")
            group_name=request.form.get("group_name")
            print("emp_id,group_name",group_name,emp_id)
            name=session["user"].get("name")
            cur = conn.cursor()
            values=cur.execute(f"select group_id from group_table where group_name='{group_name}'")
            for i in values:
                group_id=i[0]
            conn.close()
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            cur.execute(f"INSERT INTO Employee_group_map VALUES({emp_id},{group_id})")
            conn.commit()
            conn.close()
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            values=cur.execute(f"select * from Employee_group_map")
            list1=[]
            for i in values:
                conn = sqlite3.connect("database.db")
                cur = conn.cursor()
                values1=cur.execute(f"select group_name from group_table where group_ID={i[1]}")
                for j in values1:
                    data={"EMP_ID":i[0],"Group_ID":i[1],"Group_name":j[0]}
                conn.close()
                list1.append(data)
            print(list1)
            conn.close()
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            values=cur.execute(f"select first_name,email from employee where emp_id={emp_id}")
            for i in values:
                fname=i[0]
                email=i[1]
            conn.commit()
            conn.close()
            with app.app_context():
                message = f"""
                Dear {fname}
                You have been added to {group_name}.
                ."""
                
                mail=Mail(app)
                sender = 'bot091281@gmail.com'
                #receiver = 'bot091281@gmail.com'
                msg = Message(subject='SMTP e-mail test',sender=sender,recipients=[email])
                msg.body = str(message)
                mail.send(msg)         
            
            
            return render_template("group_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible")
    else:   
        if not session.get("user") or session["admin"][0]==False:
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
        else:
            print("good work")
            name=session["user"].get("name")
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            values=cur.execute(f"select * from Employee_group_map")
            
            list1=[]
            
            
            for i in values:
                conn = sqlite3.connect("database.db")
                cur = conn.cursor()
                values1=cur.execute(f"select group_name from group_table where group_ID={i[1]}")
                for j in values1:
                    data={"EMP_ID":i[0],"Group_ID":i[1],"Group_name":j[0]}
                conn.close()
                list1.append(data)
            print(list1)
            conn.close()
            return render_template("group_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible")
#for inserting
# @app.route("/crud",methods=["POST","GET"])
# def insert():
#     print("good work")
#     if request.method=="POST":

#         if not session.get("user"):
#             session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
#             return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
            
            
#         else:
            
#             conn = sqlite3.connect("database.db")
#             print("in")
#             emp_id=request.form.get("Emp_ID")
#             fname=request.form.get("fname")
#             lname=request.form.get("lname")
#             desig=request.form.get("desig")
#             email=request.form.get("email")
#             mobile=request.form.get("mobile")
#             address=request.form.get("address")
#             gender=request.form.get("gender")
#             print("gender,address",gender,address)
#             name=session["user"].get("name")
#             cur = conn.cursor()
#             cur.execute(f"INSERT INTO Employee VALUES({emp_id},'{fname}','{lname}','{desig}','{email}',{mobile},'{address}','True','False',1)")
#             conn.commit()
#             print("Executed")
#             data=[]
#             return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=data,value="hidden")
        
@app.route("/edit/<id>",methods=["POST","GET"])
def edit(id):
    
    

    if not session.get("user") or session["admin"][0]==False:
        session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
        return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        print(id)
        conn = sqlite3.connect("database.db")
        cur=conn.cursor()
        values=cur.execute(f"select * from Employee where Emp_ID={id}")
        for i in values:
            data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"enabled":i[7],"admin":i[8],"pass_id":i[9],"image":i[10],"gender":i[11]}
        name=session["user"].get("name")
        return render_template("edit_colab.html", user=(name.split(" "))[0],list=data)
@app.route("/edit/<group_id>/<emp_id>",methods=["POST","GET"])
def edit_group(group_id,emp_id):
    if not session.get("user") or session["admin"][0]==False:
        session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
        return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        print(id)
        conn = sqlite3.connect("database.db")
        cur=conn.cursor()
        values1=cur.execute(f"select group_name from group_table where group_id={group_id}")
        
        for i in values1:
            group_name=i[0]
        conn.close()
        conn = sqlite3.connect("database.db")
        cur=conn.cursor()
        values=cur.execute(f"select * from Employee_group_map where Emp_ID={emp_id} and group_id={group_id}")
        for i in values:
            data={"EMP_ID":i[0],"Group_ID":i[1],"Group_name":group_name}
        conn.close()
       
        
        
        name=session["user"].get("name")
        return render_template("group_edit_colab.html", user=(name.split(" "))[0],list=data)
@app.route("/update/<group_name>/<emp_id>/<group_id1>",methods=["POST","GET"])
def update_group(group_name,emp_id,group_id1):
    if request.method=="POST":
        if not session.get("user") or session["admin"][0]==False:
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
        else:
            conn = sqlite3.connect("database.db")
            emp_id=request.form.get("Emp_ID")
            group_name=request.form.get("group_name")
            print("emp_id,group_name",group_name,emp_id)
            name=session["user"].get("name")
            cur = conn.cursor()
            values=cur.execute(f"select group_id from group_table where group_name='{group_name}'")

            for i in values:
                group_id=i[0]
            print("group_id",group_id,values)
            conn.close()
            
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            
            cur.execute(f"""
            update Employee_group_map
            set emp_id={emp_id},
                group_id={group_id}
                where Emp_ID={emp_id} and group_id={group_id1}""")
            conn.commit()
            conn.close()
            
            name=session["user"].get("name")
            return redirect(url_for("group"))
@app.route("/delete/<group_id>/<emp_id>",methods=["POST","GET"])
def delete_group(group_id,emp_id):
    

    if not session.get("user") or session["admin"][0]==False:
        session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
        return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        conn = sqlite3.connect("database.db")
        cur=conn.cursor()
        values=cur.execute(f"delete from employee_group_map where Emp_ID={emp_id} and group_id={group_id}")
        conn.commit()
        data=[]
        name=session["user"].get("name")
        return redirect(url_for("group"))


    
    

    # if not session.get("user"):
    #     session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
    #     return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    # else:
    #     print(id)
    #     conn = sqlite3.connect("database.db")
    #     cur=conn.cursor()
    #     values=cur.execute(f"select * from Employee where Emp_ID={id}")
    #     for i in values:
    #         data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}
    #     name=session["user"].get("name")
    #     return render_template("edit_colab.html", user=(name.split(" "))[0],list=data)
@app.route("/delete/<id>",methods=["POST","GET"])
def delete(id):
    

    if not session.get("user") or session["admin"][0]==False:
        session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
        return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        conn = sqlite3.connect("database.db")
        cur=conn.cursor()
        values=cur.execute(f"delete from Employee where Emp_ID={id}")
        conn.commit()
        data=[]
        name=session["user"].get("name")
        return redirect(url_for("crud"))
@app.route("/update/<id>",methods=["POST","GET"])
def update(id):
    if request.method=="POST":
        if not session.get("user") or session["admin"][0]==False:
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
        else:
            conn = sqlite3.connect("database.db")
            cur=conn.cursor()
            
            emp_id=request.form.get("Emp_ID")
            fname=request.form.get("fname")
            lname=request.form.get("lname")
            desig=request.form.get("desig")
            email=request.form.get("email")
            mobile=request.form.get("mobile")
            address=request.form.get("address")
            gender=request.form.get("gender")
            is_admin=request.form.get("admin")
            enabled=request.form.get("enabled")
            image=request.files["image"]
            image.save(f"C:/Users/sudha/Downloads/ms-identity-python-webapp-master/static/img/{image.filename}") 
            print(f"""
            update Employee
            set emp_id={emp_id},
                first_name={fname},
                last_name={lname},
                designation={desig},
                email={email},
                mobile={mobile},
                address={address},
                is_admin='{is_admin}',
                is_enabled='{enabled}',
                gender='{gender}',
                image='{image.filename}'
                where Emp_ID={id}""")
            cur.execute(f"""
            update Employee
            set emp_id={emp_id},
                first_name='{fname}',
                last_name='{lname}',
                designation='{desig}',
                email='{email}',
                mobile='{mobile}',
                address='{address}',
                is_admin='{is_admin}',
                is_enabled='{enabled}',
                gender='{gender}',
                image='{image.filename}'
                where Emp_ID={id};""")
            conn.commit()
            data=[]
            name=session["user"].get("name")
            return redirect(url_for("crud"))
            



            
@app.route("/crud2",methods=["POST","GET"])
def seuser():
    print("in")
    if request.method=="POST":
        if not session.get("user") or session["admin"][0]==False:
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
        else:
            
            search=request.form.get("input")
            search=search.strip()
            print("search",search)
            list1=[]
            data={"EMP_ID":0,"first_name":"","last_name":"","designation":"","email":"","mobile":0,"address":"","is_enabled":"","is_admin":"","pass_id":""}
            try:
                if(int(search)):
                    try:
                        con = sqlite3.connect("database.db")
                        cur=con.cursor()
                        values=cur.execute(f"select * from Employee where Emp_ID={int(search)}")
                        if len(values.fetchall())==0:
                            raise "exception"
                        con.close()
                        con = sqlite3.connect("database.db")
                        cur=con.cursor()
                        values=cur.execute(f"select * from Employee where Emp_ID={int(search)}")


                        for i in values:
                            
                           
                            data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}
                        con.close()
                        
                        name=session["user"].get("name")
                        return render_template("crud1_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=data,value="visible")
                    except:
                        
                        return redirect(url_for("crud"))

                    
            except:
                try:
                    print("in email")
                    con = sqlite3.connect("database.db")
                    cur=con.cursor()
                    print(f"select * from Employee where email='{search}'")
                    values=cur.execute(f"select * from Employee where email='{search}'")
                    
                    if len(values.fetchall())==0:
                        raise "exception"
                    con = sqlite3.connect("database.db")
                    cur=con.cursor()
                    print(f"select * from Employee where email='{search}'")
                    values=cur.execute(f"select * from Employee where email='{search}'")
                    for i in values:
                        print("inside loop",i[0])       
                            
                        data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}
                    con.close()
                    name=session["user"].get("name")
                    print(data)
                    return render_template("crud1_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=data,value="visible")
                except:
                    return redirect(url_for("crud"))

           
            
@app.route("/segroup",methods=["POST","GET"])
def segroup():
    print("in")
    if request.method=="POST":
        if not session.get("user") or session["admin"][0]==False:
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
        else:
            
            search=request.form.get("input")
            search=search.strip()
            print("search",search)
            list1=[]
            
            try:
                if(int(search)):
                    try:
                        con = sqlite3.connect("database.db")
                        cur=con.cursor()
                        values=cur.execute(f"select * from Employee_group_map where Emp_ID={int(search)}")
                        list1=[]
                        for i in values:
                            conn = sqlite3.connect("database.db")
                            cur = conn.cursor()
                            values1=cur.execute(f"select group_name from group_table where group_ID={i[1]}")
                            for j in values1:
                                data={"EMP_ID":i[0],"Group_ID":i[1],"Group_name":j[0]}
                            conn.close()
                            list1.append(data)
                        
                        
                        con.close()
                        print(data)
                        name=session["user"].get("name")
                        return render_template("group_search.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible")
                    except:
                        try:
                            con = sqlite3.connect("database.db")
                            cur=con.cursor()
                            values=cur.execute(f"select * from Employee_group_map where group_ID={int(search)}")
                            list1=[]
                            for i in values:
                                conn = sqlite3.connect("database.db")
                                cur = conn.cursor()
                                values1=cur.execute(f"select group_name from group_table where group_ID={i[1]}")
                                for j in values1:
                                    data={"EMP_ID":i[0],"Group_ID":i[1],"Group_name":j[0]}
                                conn.close()
                                list1.append(data)
                            
                            con.close()

                            print(data)
                            name=session["user"].get("name")
                            return render_template("group_search.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible")
                        except:
                            
                            return redirect(url_for("group"))

                    
            except:
                try:
                    con = sqlite3.connect("database.db")
                    cur=con.cursor()
                    values=cur.execute(f"select group_id from group_table where group_name='{search}'")
                    if(len(values.fetchall())==0):
                        raise "exception"
                    con.close()
                    con = sqlite3.connect("database.db")
                    cur=con.cursor()
                    values=cur.execute(f"select group_id from group_table where group_name='{search}'")
                    
                    group_id=0
                    for i in values:
                        group_id=i[0]
                    con.close()
                    con = sqlite3.connect("database.db")
                    cur=con.cursor()
                    values=cur.execute(f"select * from Employee_group_map where group_ID={group_id}")
                    list1=[]
                    for i in values:
                        conn = sqlite3.connect("database.db")
                        cur = conn.cursor()
                        values1=cur.execute(f"select group_name from group_table where group_ID={i[1]}")
                        for j in values1:
                            data={"EMP_ID":i[0],"Group_ID":i[1],"Group_name":j[0]}
                        conn.close()
                        list1.append(data)
                    
                    con.close()

                    
                    name=session["user"].get("name")
                    return render_template("group_search.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible")
                except:
                    return redirect(url_for("group"))
        

            


@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session["users"]=[]
    session.clear() # Wipe out user and its token cache from session
    print("This",url_for("index",_external=True))
    #return redirect(url_for("index"))
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))
    

@app.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

if __name__ == "__main__" :
    app.debug=True
    app.run(host="127.0.0.1",port=5000)

