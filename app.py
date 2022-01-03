import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config
import sqlite3
con=sqlite3.connect("database.db")


app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route("/")
def index():
    if not session.get("user"):
       session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
       return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    
    name=session["user"].get("name")
    
    return render_template("after.html", user=(name.split(" "))[0], version=msal.__version__)
@app.route("/search")
def search():
    if not session.get("user"):
       session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
       return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    
    name=session["user"].get("name")
    
    return render_template("search_colab.html", user=(name.split(" "))[0], version=msal.__version__)
@app.route("/crud",methods=["POST","GET"])
def crud():
    if request.method=="POST":
        print("in")
        if not session.get("user"):
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
            print("gender,address",gender,address)
            name=session["user"].get("name")
            cur = conn.cursor()
            cur.execute(f"INSERT INTO Employee VALUES({emp_id},'{fname}','{lname}','{desig}','{email}',{mobile},'{address}','True','False',1)")
            conn.commit()
            conn.close()
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            values=cur.execute("select * from employee")
            list1=[]

            for i in values:
                data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}
                list1.append(data)
            conn.close()
            print("Executed")
            
            return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible")
    else:   
        if not session.get("user"):
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
            return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible")
@app.route("/group",methods=["POST","GET"])
def group():
    if request.method=="POST":
        print("in")
        if not session.get("user"):
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
            values=cur.execute(f"select * from employee_group_map")
            list1=[]
            print("group_name: ",group_name)
            for i in values:
                data={"EMP_ID":i[0],"Group_ID":i[1],"Group_name":group_name}
                list1.append(data)
            print(data)
            conn.commit()
            conn.close()
                     
            
            
            return render_template("group_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=list1,value="visible")
    else:   
        if not session.get("user"):
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
    
    

    if not session.get("user"):
        session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
        return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        print(id)
        conn = sqlite3.connect("database.db")
        cur=conn.cursor()
        values=cur.execute(f"select * from Employee where Emp_ID={id}")
        for i in values:
            data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}
        name=session["user"].get("name")
        return render_template("edit_colab.html", user=(name.split(" "))[0],list=data)
@app.route("/edit/<group_id>/<emp_id>",methods=["POST","GET"])
def edit_group(group_id,emp_id):
    if not session.get("user"):
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
        if not session.get("user"):
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
            print(f"""
            update Employee_group_map
            set emp_id={emp_id},
                group_id={group_id}
                where Emp_ID={emp_id} and group_id={group_id}""")
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
    

    if not session.get("user"):
        session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
        return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        conn = sqlite3.connect("database.db")
        cur=conn.cursor()
        values=cur.execute(f"delete from employee_group_map where Emp_ID={emp_id} and group_id={group_id}")
        conn.commit()
        data=[]
        name=session["user"].get("name")
        return render_template("group_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=data,value="hidden")


    
    

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
    

    if not session.get("user"):
        session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
        return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
    else:
        conn = sqlite3.connect("database.db")
        cur=conn.cursor()
        values=cur.execute(f"delete from Employee where Emp_ID={id}")
        conn.commit()
        data=[]
        name=session["user"].get("name")
        return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=data,value="hidden")
@app.route("/update/<id>",methods=["POST","GET"])
def update(id):
    if request.method=="POST":
        if not session.get("user"):
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
            print(f"""
            update Employee
            set emp_id={emp_id},
                first_name={fname},
                last_name={lname},
                designation={desig},
                email={email},
                mobile={mobile},
                address={address}
                where Emp_ID={id}""")
            cur.execute(f"""
            update Employee
            set emp_id={emp_id},
                first_name='{fname}',
                last_name='{lname}',
                designation='{desig}',
                email='{email}',
                mobile='{mobile}',
                address='{address}'
                where Emp_ID={id};""")
            conn.commit()
            data=[]
            name=session["user"].get("name")
            return redirect(url_for("crud"))
            



            
@app.route("/crud2",methods=["POST","GET"])
def seuser():
    print("in")
    if request.method=="POST":
        if not session.get("user"):
            session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) 
            return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)
        else:
            con = sqlite3.connect("database.db")
            search=request.form.get("input")
            search=search.strip()
            print("search",search)
            list1=[]
            data={"EMP_ID":0,"first_name":"","last_name":"","designation":"","email":"","mobile":0,"address":"","is_enabled":"","is_admin":"","pass_id":""}
            try:
                if(int(search)):
                    
                    cur=con.cursor()
                    values=cur.execute(f"select * from Employee where Emp_ID={int(search)}")
                    
                    for i in values:
                        data={"EMP_ID":i[0],"first_name":i[1],"last_name":i[2],"designation":i[3],"email":i[4],"mobile":i[5],"address":i[6],"is_enabled":i[7],"is_admin":i[8],"pass_id":i[9]}

                    print(data)
                    name=session["user"].get("name")
                    return render_template("crud1_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=data,value="visible")
                    
            except:
                
                cur=con.cursor()
                cur.execute(f"select * from Employee where email={search}")
                data=cur.fetchall()
                name=session["user"].get("name")
                
                return render_template("crud1_colab.html", user=(name.split(" "))[0], version=msal.__version__,list=data,value="visible")
                

            # name=session["user"].get("name")
            # return render_template("crud_colab.html", user=(name.split(" "))[0], version=msal.__version__)



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
    return redirect(url_for("index"))
    # return redirect(  # Also logout from your tenant's web session
    #     app_config.AUTHORITY + "/oauth2/v2.0/logout" +
    #     "?post_logout_redirect_uri=" + url_for("index", _external=True))
    

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

