from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 사용자 데이터
users = [
    {"username": "traveler", "name": "Alex"},
    {"username": "photographer", "name": "Sam"},
    {"username": "gourmet", "name": "Chris"}
]

# 사용자 목록 페이지
@app.route('/')
def index():
    return render_template('index.html', users=users)

# 사용자 추가
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        users.append({'username': username, 'name': name})
        return redirect(url_for('index'))
    return render_template('add_user.html')

# 사용자 수정
@app.route('/edit/<username>', methods=['GET', 'POST'])
def edit_user(username):
    user = next((u for u in users if u['username'] == username), None)
    if user is None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user['name'] = request.form['name']
        return redirect(url_for('index'))
    return render_template('edit_user.html', user=user)

# 사용자 삭제
@app.route('/delete/<username>')
def delete_user(username):
    global users
    users = [u for u in users if u['username'] != username]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)