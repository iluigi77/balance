# API BALANCE
https://github.com/iluigi77/balance.git

## pre requirements
* python >= 3.6.9 
* adobe acrobat reader
## Install
#### **create viertualenv**
~~~ 
py -3 -m venv venv
~~~

#### **activate enviroment**

#### **install requirements**
~~~
pip install -r requirements.txt
~~~  
#### create .env file
~~~
SECRET_KEY=yousecrretkey
API_KEY=youapikey
CSRF_ENABLED=True
~~~

#### duplicate template.ini as config.ini


## run gunicorn
gunicorn --bind 0.0.0.0:5000 wsgi:app
## run waitress
waitress-serve --port=5000 wsgi:app

## run dev (linux)
