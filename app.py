from flask import Flask
from config import Config
from routes.r import register_blueprints

# 初始化 Flask
app = Flask(__name__)
app.config.from_object(Config)

# 注册所有蓝图
register_blueprints(app)

@app.route("/",methods=["GET"])
def home():
    return "后端服务启动成功！"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
