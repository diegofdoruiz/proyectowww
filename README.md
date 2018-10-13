# Django 2.1.2 - Python 3.6.4. Project to handle shifts of a bank.

# Global requirements
	- Python 3.6.4
	- pip3
	- virtualenv

# Local env requiremenst
	- Django==2.1.2
	- psycopg2==2.7.5
	- psycopg2-binary==2.7.5

# DB - Postgresql 10
	- create user www with password 'www'
	- alter user with superuser createrole createdb
	- Create database proyectowww with owner 'www'

# How to use it
	path$ mkdir localfolder
	path$ cd localfolder
	path/localfolder$ virtualenv env -p python3
	path/localfolder$ source env/bin/activate
	(env)path/localfolder$ cd proyectowww       (cloned and decompressed project) 
	(env)path/localfolder/proyectowww$ pip3 install -r requirements.txt    (in this folder init git, add . commit, ....)
	(env)path/localfolder/proyectowww$ cd proyectoprincipal
	(env)path/localfolder/proyectowww/proyectoprincipal$ python3 manage.py makemigrations
	(env)path/localfolder/proyectowww/proyectoprincipal$ python3 manage.py migrate
	(env)path/localfolder/proyectowww/proyectoprincipal$ python3 manage.py runserver