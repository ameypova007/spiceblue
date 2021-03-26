from flask import Flask
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect

connect("mongodb+srv://ameym:root@cluster0.3vy1j.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
app = Flask(__name__)
app.config['SECRET_KEY'] = "5791428bb0b13ce0c676dfqw280ba29233230"

from sound import routes



