"""
BF6 玩家数据查询 Web 应用
提供网页界面查询和展示多个玩家的统计数据
"""

from flask import Flask, render_template, jsonify, Response
import asyncio
import os
import json
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
    """API端点：获取所有玩家数据（带进度）"""
    def generate():
        """生成器函数，流式返回数据"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # 存储进度和结果
        progress_data = {'current': 0, 'total': 0, 'name': ''}
        results = []
        
        async def progress_callback(current, total, name):
            """进度回调"""
            progress_data['current'] = current
            progress_data['total'] = total
            progress_data['name'] = name
            # 发送进度更新
            yield f"data: {json.dumps({'type': 'progress', 'current': current, 'total': total, 'name': name})}\n\n"
        
        async def fetch_with_progress():
            """带进度的获取函数"""
            async def callback(current, total, name):
                progress_data['current'] = current
                progress_data['total'] = total
                progress_data['name'] = name
            
            return await fetch_all_players_data(progress_callback=callback)
        
        try:
            # 先发送开始信号
            yield f"data: {json.dumps({'type': 'start'})}\n\n"
            
            # 获取数据
            players_data = loop.run_until_complete(fetch_with_progress())
            
            # 发送完成信号和数据
            yield f"data: {json.dumps({'type': 'complete', 'data': players_data})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        finally:
            loop.close()
    
    # 尝试使用SSE，如果不支持则降级为普通JSON
    try:
        # 简化版本：直接返回数据，不使用SSE（因为实现复杂）
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

