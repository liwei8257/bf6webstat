"""
生产环境WSGI入口文件
用于Gunicorn等WSGI服务器
"""
from app import app

if __name__ == "__main__":
    app.run()

