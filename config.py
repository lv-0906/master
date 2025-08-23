import os
from dotenv import load_dotenv
import mysql.connector

# 加载 .env 文件
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "lipe"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "")
    }

def get_db_connection():
    return mysql.connector.connect(**Config.DB_CONFIG)