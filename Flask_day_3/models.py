# Model -> Table 생성
# 게시글 - board
# 유저 - user

from db import db

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  address = db.Column(db.String(200), nullable=False)
  boards = db.relationship('Board', back_populates='author', lazy='dynamic')
  
class Board(db.Model):
  __tablename__ = 'boards'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  author = db.relationship('User', back_populates='boards')