import os
from flask import redirect, abort, jsonify,request,url_for, make_response, Flask
from flask_sqlalchemy import SQLAlchemy
import jwt
from sound.models import User, Template
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sound.app import app, db
from sound.token_verifier import token_required
import uuid 

@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
    data = request.get_json()  
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(token_id=str(uuid.uuid4()),firstname=data['first_name'], lastname = data['last_name'], emailid = data['emailid'], password = hashed_password) 
    db.session.add(new_user)  
    db.session.commit()    
    return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
    data = request.get_json()
    user = User.query.filter_by(firstname=data["first_name"]).first()   
    if check_password_hash(user.password, data["password"]):  
        token = jwt.encode({'user_id': user.token_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        print(token)
        return jsonify({'token' : token}) 

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/template', methods=['POST', 'GET'])
@token_required
def create_templates(current_user):
    print(request.method)
    if request.method == "POST":   
        data = request.get_json() 
        new_template = Template(name=data['template_name'], subject=data['subject'], body=data['body'], user_id=current_user.id)  
        db.session.add(new_template)   
        db.session.commit()
        return jsonify({'message' : 'new template has been created'}) 

    elif request.method == "GET":
        template = Template.query.filter_by(user_id = current_user.id)
        print(template)
        responses = []
        for i in template:
            response = {}
            response["id"] = i.id
            response["name"] = i.name
            response["subject"] = i.subject
            response["body"] = i.body
            responses.append(response)
        return jsonify(responses)

@app.route("/template/<template_id>", methods=['PUT'])
@token_required
def update_template(current_user,template_id):
    temp = Template.query.filter_by(id =template_id, user_id = current_user.id).first()

    if not temp:   
       return jsonify({'message': 'invalid user id  or template does not exist'})

    data = request.get_json() 
    # print(temp.body)
    temp.name=data['template_name'] 
    temp.subject=data['subject']
    temp.body=data['body'] 
    db.session.commit()
    return jsonify({"message":"Template updated"})


@app.route("/template/<template_id>", methods=['DELETE'])
@token_required
def delete_template(current_user,template_id):
    temp = Template.query.filter_by(id =template_id, user_id = current_user.id).first()

    if not temp:   
       return jsonify({'message': 'invalid user id  or template does not exist'})

    db.session.delete(temp)
    db.session.commit()
    return jsonify({"message":"Template deleted"})