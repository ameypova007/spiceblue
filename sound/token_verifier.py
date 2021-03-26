from flask import request,jsonify
import jwt
from sound.models import User, Template
from sound.app import app
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
         print(data)
         current_user = User.objects.get({'token_id' :data['user_id']})
      except:
         return jsonify({'Message': 'token is invalid'})
      return f(current_user, *args, **kwargs)
   return decorator
