from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from config import get_db_connection

upload_bp = Blueprint('upload', __name__, url_prefix='/api')

UPLOAD_FOLDER = "uploads/images"
# 创建上传文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png","jpg","jpeg","webp"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload",methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "没有文件"}), 400 
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        orders_id = request.form.get("orders_id")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET image_url = %s where id = %s", (filepath,orders_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "url": f"/{filepath}"})
    return jsonify({"status": "error", "message": "不支持的文件类型"}), 400