from flask import Flask, render_template, jsonify, request, redirect, url_for
import jwt
import hashlib
import datetime
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbMember

SECRET_KEY = 'HelloFlask'

app = Flask(__name__)
# 로그인
@app.route('/login')
def home():
    return render_template('member/login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id']
    password_receive = request.form['password']
    
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'user_id': id_receive, 'password': password_hash})
    
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'success': True, 'token': token})
    else:
        return jsonify({'success': False, 'msg': '아이디/비밀번호가 일치하지 않습니다'})
    
# 아이디 중복 체크
def isDuplicate(_id):
    if db.user.find_one({'user_id': _id}):
        return True
    return False

@app.route('/api/id_check', methods=['POST'])
def idCheck():
    _id = request.form['id']
    if isDuplicate(_id):
        return jsonify({'success': False, 'msg': '중복된 아이디입니다.'})
    return jsonify({'success': True, 'msg': '사용 가능한 아이디입니다.'})

# 회원가입
@app.route('/register', methods=['GET'])
def register():
    return render_template('member/register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    result = request.form
    _id = result['id']
    if isDuplicate(_id):
        return jsonify({'success': False, 'msg': '중복된 아이디입니다.'})
    _password = result['password']
    _password_hash = hashlib.sha256(_password.encode('utf-8')).hexdigest()
    _name = result['nick_name']
    _gender = result['gender']
    
    db.user.insert_one({'user_id': _id, 'password': _password_hash, 'name': _name, 'gender': _gender})
    return jsonify({'success': True, 'msg': '로그인 페이지로 이동합니다.'})
    
    
if __name__ == '__main__':
    app.run(debug=True)
