create_employees_table = """
        create table if not exists Employee (
            emp_id integer primary key,
            first_name text not null,
            last_name text Default " ",
            designation text Default "Not Assigned",
            email text Default "NA",
            mobile text Defaut "NA",
            address text Default "NA",
            is_enabled text not null,
            is_admin text not null,
            pass_id text not null
        );
    """
    
create_group_table = """
    create table if not exists Group_table (
        group_id integer primary key,
        group_name text not null,
        group_desc text not null
    );
"""

create_password_table = """
    create table if not exists Password (
        pass_id integer primary key,
        password text not null,
        creation_date timestamp not null,
        expiry_date timestamp not null,
        password_history text 
    );
"""

create_admin_group_mapping = """
    create table if not exists Admin_group_map (
        emp_id integer not null UNIQUE,
        group_id integer not null UNIQUE,
        FOREIGN KEY(emp_id) REFERENCES Employee(emp_id),
        FOREIGN KEY(group_id) REFERENCES Employee(group_id)
    )
"""

employee_data =[
    (101, "abc","def","","","999","abcd",1,"True", "True"),
    (102, "def","","P2","def@d.com","998","efgh",2,"True", "False"),
    (103, "ghi", "jkl", "P2", "","997","ijkl",3,"True", "False"),
    (104, "jkl", "lmn", "P2", "jkl@d.com","996","mnop",4,"True", "False")
]

password_data = [
    (1,"ab12",'31/12/2099'),
    (2,"cb34",'31/12/2099'),
    (3,"ef56",'31/12/2099'),
    (4,"gh78",'31/12/2099')
]

admin_data = [
    (101,"AdminTheGreat", "password1")    
]

group_data = [
    ("Group-1", "First Group"),
    ("Group-2", "Second group"),
    ("Group-3", "Third Group")    
]


# ["emp_id", "username", "first_name", "last_name", "designation", "email", "group_id", "mobile", "address", "is_enabled", "is_admin", "pass_id"]