1. create database account with table user, as shown below
    
    create table user(
        id integer not null auto_increment,
        username varchar(30) not null,
        email varchar(40) not null,
        password varchar(40) not null,
        PRIMARY KEY(id)
    );

2. setup code as specified

3. run the following in the terminal:
    >> export flask_app=app.py
    >> export flask_env=development
    >> flask run

4. website will be running on http://127.0.0.1:5000/