from datetime import datetime
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect

class User(MongoModel):
	firstname = fields.CharField(max_length=60, required=True)
	lastname = fields.CharField(max_length=60, required=True)
	password = fields.CharField(max_length=100000000, required=True)
	token_id = fields.CharField()
	emailid = fields.CharField(max_length=100, required=True,primary_key=True)

class Template(MongoModel):
	name = fields.CharField(max_length=60, required=True)
	subject =fields.CharField(max_length=60, required=True)
	body = fields.CharField(max_length=60, required=True)
	user_id = fields.ReferenceField(User)
