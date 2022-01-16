from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    movie_star = list(db.mystar.find({},{'_id':False}).sort('like', -1)) #like로 정렬
    return jsonify({'movie_stars': movie_star})


@app.route('/api/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']
    target_star = db.mystar.find_one({'name': name_receive})
    current_like = target_star['like']

    new_like = current_like + 1
    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})
    return jsonify({'msg': '좋아요 완료!'})
    #좋아요한 이름을 받아서 그것의 좋아요를 1 증가 시킨다.

@app.route('/api/delete', methods=['POST'])
def delete_star():
    name_receive = request.form['name_give']
    db.mystar.delete_one({'name':name_receive})
    return jsonify({'msg': '삭제 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)