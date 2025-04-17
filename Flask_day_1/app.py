from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # 사용자 데이터 정의
    users = [
        {"username": "traveler", "name": "Alex"},
        {"username": "photographer", "name": "Sam"},
        {"username": "gourmet", "name": "Chris"}
    ]
    
    # 사용자 목록을 템플릿으로 전달
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
