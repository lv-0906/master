from flask import Blueprint, jsonify, request
from config import get_db_connection

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")
@orders_bp.route("/")
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    familyid = request.args.get("familyid")
    cursor.execute("SELECT * FROM orders where family_id = %s",(familyid))  
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(orders)
@orders_bp.route("/createorder",methods=["post"])
def create_order():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()
    cursor.execute("INSERT INTO orders(family_id,user_id,dishes,image_url)VALUES(%s,%s,%s,%s)",(data["familyid"],data["userid"],data["dishes"],data["image_url"]))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status":"success"})