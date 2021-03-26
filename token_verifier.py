from flask import request,jsonify
import jwt
from sound.models import User, Template
from sound.app import app, db
from functools import wraps


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None


      if 'Authorization' in request.headers:
         token = request.headers['Authorization']

      if token is None:
         return jsonify({'message': 'a valid token is missing'})


      try:
         data = jwt.decode(token[7:], app.config['SECRET_KEY'], algorithms="HS256")
         current_user = User.query.filter_by(token_id=data['user_id']).first()
      except:
         return jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator


   # Headers : {
   #              'Authorization': 'Bearer ' + <access_token from login step>,
   #              'Accept': 'application/json',
   #              'Content-Type': 'application/json',          
   #            }
   #  Body :    {
   #              'template_name': ' ',
   #              'subject': ' ',
   #              'body': ' ',
   #                   } 