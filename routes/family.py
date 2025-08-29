from flask import Blueprint, jsonify, request
from config import get_db_connection
from sqlalchemy import text
from datetime import datetime, timedelta
import uuid

family_bp = Blueprint("family", __name__, url_prefix="/family")
@family_bp.route("/")
def get_family():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    familyid = request.args.get("id")
    cursor.execute("SELECT * FROM family where id = %s",(familyid))  
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
@family_bp.route("/joinfamily",methods=["post"])
def join_family_by_code():
    conn = get_db_connection()
    data = request.get_json()
    code = data["code"]
    try:
        conn.start_transaction() 
        with conn.cursor(dictionary=True) as cursor:
            # 检查邀请码是否存在且未过期
            cursor.execute("SELECT * FROM invite_codes WHERE code = %s AND expire_at > NOW()", (code,))
            invite = cursor.fetchone()
            if not invite:
                return jsonify({"status": "error", "message": "邀请码无效或已过期"}), 400
            familyid = invite["family_id"]
            userid = invite["user_id"]
            # 检查 family 是否存在
            cursor.execute("SELECT * FROM family WHERE id = %s", (familyid,))
            family = cursor.fetchone()
            if not family:
                return jsonify({"status": "error", "message": f"家庭 {familyid} 不存在"}), 400
            # 检查用户是否已加入家庭
            cursor.execute("SELECT family_id FROM users WHERE id = %s", (userid,))
            user = cursor.fetchone()
            if not user:
                return jsonify({"status": "error", "message": f"用户 {userid} 不存在"}), 400
            if user["family_id"]:
                return jsonify({"status": "error", "message": f"用户 {userid} 已加入家庭"}), 400
            # 更新用户表，绑定家庭
            cursor.execute("UPDATE users SET family_id = %s WHERE id = %s", (familyid, userid))
            # 更新 family 表的 count (+1)
            cursor.execute("UPDATE family SET user_count = user_count + 1 WHERE id = %s", (familyid,))
        conn.commit()
        return jsonify({"status": "success", "message": "加入家庭成功"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        conn.close()
@family_bp.route("/exitfamily",methods=["post"])
def exit_family():
    conn = get_db_connection()
    data = request.get_json()
    userid = data["id"]
    try:
        with conn.cursor() as cursor:
            # 1. 检查用户是否已加入家庭
            cursor.execute("SELECT family_id FROM users WHERE id = %s", (userid,))
            user = cursor.fetchone()
            if not user:
                return jsonify({"status": "error", "message": f"用户 {userid} 不存在"}), 400
            if not user["family_id"]:
                return jsonify({"status": "error", "message": f"用户 {userid} 未加入家庭"}), 400
            # 2. 更新用户表，解绑家庭
            cursor.execute("UPDATE users SET family_id = NULL WHERE id = %s", (userid,))
            # 3. 更新 family 表的 count (-1)
            cursor.execute("UPDATE family SET user_count = user_count - 1 WHERE id = %s", (user["family_id"],))
            cursor.execute("SELECT user_count FROM family WHERE id = %s",(user["family_id"],))
            count = cursor.fetchone()
            if not count["user_count"] == 0:
                return jsonify({"status": "success", "message": "退出家庭成功"})
            cursor.execute("DELETE FROM family WHERE id = %s",(user["family_id"],))
                # 如果家庭人数为0时 删除家庭
        conn.commit()
        return jsonify({"status": "success", "message": "退出家庭成功,家庭已解散"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        conn.close()
@family_bp.route("/invitefamily",methods=["post"])
def create_invitation_code():
    conn = get_db_connection()
    data = request.get_json()
    familyid = data["familyid"]
    userid = data["id"]
    try:
        with conn.cursor() as cursor:
            code = str(uuid.uuid4())[:8]
            expire_at = datetime.now() +timedelta(minutes=5)
            cursor.execute("INSERT INTO invite_codes (family_id,code,expire_at,user_id) VALUES (%s,%s,%s,%s)",(familyid,code,expire_at,userid))
        conn.commit()
        return jsonify({"status": "success", "invite_code": code, "expire_at": expire_at.strftime("%Y-%m-%d %H:%M:%S")})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        conn.close()