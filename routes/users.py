from flask import Blueprint, jsonify,request
from config import get_db_connection
from db_utils import is_value_exists


users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/adduser', methods=['POST'])
def add_user():
    data = request.json
    open_id = data['open_id']
    nickname = data['nickname']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if is_value_exists('users','nickname',nickname):
            return jsonify({"message": "用户昵称已存在"}), 400
        if is_value_exists('users','open_id',open_id):
            return jsonify({"message": "当前用户已存在"}), 400
        cursor.execute("INSERT INTO users (nickname,open_id) VALUES (%s,%s)", (nickname,open_id))
        conn.commit()
        return jsonify({"message": "用户注册成功"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400
@users_bp.route('/getuser')
def get_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    openid = request.json['open_id']
    try:
        cursor.execute("SELECT * FROM users where open_id=%s",(openid,))
        users = cursor.fetchall()
        return jsonify(users)
    except Exception as e:
        return jsonify({"message": str(e)}), 400
