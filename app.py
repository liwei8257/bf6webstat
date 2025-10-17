"""
BF6 玩家数据查询 Web 应用
提供网页界面查询和展示多个玩家的统计数据
"""

from flask import Flask, render_template, jsonify
import asyncio
import os
from data_processor import fetch_all_players_data, load_players_config

app = Flask(__name__)

# 加载配置
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')


@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')


@app.route('/api/players')
def get_players_data():
    """API端点：获取所有玩家数据"""
    try:
        # 在新的事件循环中运行异步函数
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        players_data = loop.run_until_complete(fetch_all_players_data())
        loop.close()
        
        return jsonify({
            'success': True,
            'data': players_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/players/config')
def get_players_config():
    """API端点：获取配置的玩家列表"""
    try:
        config = load_players_config()
        return jsonify({
            'success': True,
            'data': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 BF6玩家数据查询系统启动中...")
    print("📊 访问: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

