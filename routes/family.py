from flask import Blueprint, jsonify, request
from config import get_db_connection


family_bp = Blueprint("family", __name__, url_prefix="/family")
@family_bp.route("/")
def get_family():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM family")  
    family = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(family)

@family_bp.route("/",methods=["POST"])
def add_family():
    conn = get_db_connection()
    data = request.get_json()
    name = data["nickname"]
    family_type = data["family_type"] if "family_type" in data else 1
    try:
        with conn.cursor() as cursor:
            # 先查重
            check_sql = "SELECT id FROM family WHERE nickname = %s"
            cursor.execute(check_sql, [name])
            exist = cursor.fetchone()
            if exist:
                return jsonify({"status": "error", "message": f"昵称 {name} 已存在"}), 400
            # 插入数据
            sql = "INSERT INTO family (nickname, family_type) VALUES (%s, %s)"
            cursor.execute(sql, (name, family_type))
        conn.commit()
        return jsonify({"status": "success", "message": "新建家庭成功", "family": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        conn.close()