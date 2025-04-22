from flask import request, jsonify
from flask_smorest import Blueprint, abort

def create_posts_blueprint(mysql):
  posts_blp = Blueprint("posts",__name__, description="Operations on posts", url_prefix="/posts")

  @posts_blp.route('/', methods=['GET', 'POST'])
  def posts():
    
    cursor = mysql.connection.cursor()
    
    # 게시글 조회
    if request.method == 'GET':
      sql = "SELECT * FROM posts"
      cursor.execute(sql)
      
      posts = cursor.fetchall()
      cursor.close()
      
      post_list = []
      
      for post in posts:
        post_list.append({
          'id' :post[0],
          'title' :post[1],
          'content' :post[2]
        })
        
      return jsonify(post_list)
    
    # 게시글 생성
    elif request.method == 'POST':
      title = request.json.get('title')      
      content = request.json.get('content')        
      
      if not title or not content:
        abort(400, message="Title or Content cannot be emppty")    
        
      sql = 'INSERT INTO posts(title, content) VALUES(%s, %s)'
      cursor.execute(sql, (title,content))
      mysql.connection.commit()
      
      return jsonify({'msg': "successfully created post data", "title":title, "content":content}), 201
    
    # 게시글 수정 및 삭제
    # 특정 게시글만 조회하고싶을 경우
  @posts_blp.route('/<int:id>', methods=["GET", "PUT", "DELETE"])
  def post(id):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM posts WHERE id=%s"
    cursor.execute(sql, (id,))
    post = cursor.fetchone()
      
    if request.method == 'GET':
            
      if not post:
        abort(404, "Not found post")
      return ({
          'id' :post[0],
          'title' :post[1],
          'content' :post[2]
        })
        
    elif request.method == 'PUT':
      # data = request.json # 이렇게 작업해도된다.
      # title = data['title']
      
      title = request.json.get('title')
      content = request.json.get('content')
      
      if not title or not content:
        abort(400, "Not Found Title, Content")
      
      if not post:
        abort(404, "Not Found Post")
          
      sql = "UPDATE posts SET title = %s, content = %s WHERE id = %s"
      cursor.execute(sql, (title, content, id))  # title, content, id를 튜플로 전달
      mysql.connection.commit()
      
      return jsonify({"msg": "Successfully updated title and content"})
    
    elif request.method == 'DELETE':
      if not post:
        abort(400, "Not Found Title, Content")
      sql = "DELETE FROM posts WHERE id=%s"
      cursor.execute(sql, (id,))
      mysql.connection.commit()

      return jsonify({"msg":"Successfully deleted title and content"})
    
  return posts_blp