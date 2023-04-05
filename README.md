# Description

API for Medical Laboratory Inventory Management System (MLI). The system allows lab technician to set up accounts for patients and add them to group. Setting up new account requires patients to provide OTP send via their emails to admins. Admins can add patients to specific groups and CRUD their records.  

# Architechture
![image](https://user-images.githubusercontent.com/129918405/230024133-e5b71184-f7a5-4c3e-a7b1-daba51fc80bc.png)


# Installation
### Set up
$ git clone https://github.com/QuanBui-CMCGlobal/Revgov_Test

$ cd Revgov_Test

##### Create Virtual Environment
```shell
virtualenv venv
cd venv/Scripts/activate
```

##### Install dependency
```shell
pip install -r requirements.txt
```


Once download finished:
```shell
(env)$ cd project
(env)$ python manage.py runserver
```

Then navigate to **http://127.0.0.1:8000/api**

# Run API
Import [MLI.postman_collection.json](/MLI.postman_collection.json) in Postman



