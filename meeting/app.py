from flask import Flask, render_template, jsonify, request, redirect, url_for
import jwt
import hashlib
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient('localhost', 27017)
db = client.dbMember
dbpost = client.dbpost


SECRET_KEY = 'HelloFlask'

app = Flask(__name__)
# 메인페이지
@app.route('/home')
def home():
    return render_template('index.html')

# 로그인
@app.route('/login')
def login():
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

@app.route('/create')
def create():
   return render_template('broad/create.html')

@app.route('/api/create', methods=['POST'])
def create_article():
    # 1. 클라이언트로부터 데이터를 받기
    title_receive = request.form['title_give'] 
    intro_receive = request.form['intro_give'] 
    people_receive = request.form['people_give']
    sdate_receive = request.form['sdate_give']
    edate_receive = request.form['edate_give']
    fplace_receive = request.form['fplace_give']
    splace_receive = request.form['splace_give']
    desc_receive = request.form['desc_give']

    article = {'title': title_receive, 'intro': intro_receive, 'people': people_receive, 'sdate': sdate_receive, 'edate': edate_receive, 'fpalce': fplace_receive, 'splace': splace_receive, 'desc': desc_receive}
   
    # 3. mongoDB에 데이터를 넣기
    dbpost.articles.insert_one(article)

    return jsonify({'result': 'success'})

@app.route('/api/create', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 모든 데이터 조회해오기 (Read)
    result = []
    pre_result = list(dbpost.articles.find({}))
    for document in pre_result:
        document['_id'] = str(document['_id']) # string 변환
        result.append(document)
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'articles': result})
    
if __name__ == '__main__':
    app.run(debug=True)
