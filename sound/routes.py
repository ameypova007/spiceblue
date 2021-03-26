import os
from flask import redirect, abort, jsonify,request,url_for, make_response, Flask
import jwt
from sound.models import User, Template
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sound.app import app
from sound.token_verifier import token_required
import uuid
from bson.objectid import ObjectId

#signup
@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(token_id=str(uuid.uuid4()),firstname=data['first_name'], lastname = data['last_name'], emailid = data['emailid'], password = hashed_password) 
    new_user.save()
    return jsonify({'message': 'User has been Registered successfully'})

#login
@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
    data = request.get_json()
    usr = User.objects.get({'_id': data["emailid"]})  
    if check_password_hash(usr.password, data["password"]):  
        token = jwt.encode({'user_id': usr.token_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        print(token)
        return jsonify({'token' : token}) 
    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

#create template
@app.route('/template', methods=['POST', 'GET'])
@token_required
def create_templates(current_user):
    if request.method == "POST":   
        data = request.get_json() 
        try:
            new_template = Template(name=data['template_name'], subject=data['subject'], body=data['body'], user_id=current_user.emailid)  
            new_template.save()
            message = "Template has been created"
        except:
            message = "Error!,Please check the request"
        return jsonify({'message' : message}) 

    elif request.method == "GET":
        template = Template.objects.all()
        if template is None:
            return jsonify({"Message":"No Templates Found"})
        responses = []
        for i in template:
            print(i)
            response = {}
            response["id"] = str(i._id)
            response["name"] = i.name
            response["subject"] = i.subject
            response["body"] = i.body
            responses.append(response)
        return jsonify({"Template":responses})

#get specific template
@app.route("/template/<template_id>", methods=['GET'])
@token_required
def single_template(current_user,template_id):
    templates = {}
    try:
        temp = Template.objects.get({'_id':ObjectId(template_id)})
        if not temp:   
           return jsonify({'message': 'Invalid User Id  or Template does not exists'})
        templates["name"] = temp.name
        templates["subject"] = temp.subject 
        templates["body"]= temp.body
    except:
        pass
    return jsonify({"Template":templates})

#update specific template
@app.route("/template/<template_id>", methods=['PUT'])
@token_required
def update_template(current_user,template_id):
    data = request.get_json()
    temp = Template.objects.raw({'_id':ObjectId(template_id)}).update({"$set":{"name":data['template_name'],"body":data["body"],"subject":data["subject"]}})
    if not temp:   
       return jsonify({'message': 'Invalid User Id  or Template does not exists'})
    return jsonify({"message":"Template has been Updated"})

#delete specific template
@app.route("/template/<template_id>", methods=['DELETE'])
@token_required
def delete_template(current_user,template_id):
    temp = Template.objects.raw({'_id':ObjectId(template_id)}).delete()
    if not temp:   
       return jsonify({'message': 'Invalid User Id  or Template does not exists'})
    return jsonify({"message":"Template has been deleted"})
