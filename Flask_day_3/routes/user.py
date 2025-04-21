from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
from models import User

user_blp=Blueprint("Users", "users", description="Operations on users", url_prefix="/users")


# API LIST:
# (1) 전체 유저 데이터 조회(GET)

@user_blp.route('/')
class UserList(MethodView):
  def get(self):
    users = User.query.all()
    
    user_data = [
        {
      'id': user.id,
      'username': user.username,
      'email': user.email
    } for user in users
    ]

    return jsonify(user_data)
  
  # (2) 유저 생성 (POST)
  
  def post(self):
    data = request.json
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201
  

# (1) 특정 유저 데이터 조회(GET)
@user_blp.route('/<int:user_id>')
class UserResource(MethodView):
  def get(self, user_id):
    user = User.query.get_or_404(user_id)    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })
    
# (2) 특정 유저 데이터 수정(PUT)
  def put(self, user_id):    
    data = request.json
    user = User.query.get_or_404(user_id)
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})
  

# (3) 특정 유저 데이터 삭제(DELETE)
  def delete(self, user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})