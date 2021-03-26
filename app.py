# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# # from flask_mysqldb import MySQL

# # # from flask_bcrypt import Bcrypt
# # # from flask_login import LoginManager

# app = Flask(__name__)
# # # app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///templates.db'
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# db = SQLAlchemy(app)
# # # bcrypt = Bcrypt(app)
# # # login_manager = LoginManager(app)
# # # login_manager.login_view = 'login'
# # # login_manager.login_message_category = 'info'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "5791428bb0b13ce0c676dfqw280ba290"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///templates.db'
# app.config['MONGO_URI'] = "mongodb://ameym:root123@cluster0.3vy1j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

from sound import routes



