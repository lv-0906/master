from flask import Blueprint, jsonify,request
from config import get_db_connection


users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/user', methods=['POST'])
def add_user():
    data = request.json
    nickname = data['nickname']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (nickname) VALUES (%s)",
            (nickname)
        )
        conn.commit()
        return jsonify({"message": "用户注册成功"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400

