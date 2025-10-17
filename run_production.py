"""
生产环境启动脚本（Windows适用）
使用waitress作为WSGI服务器
"""
import os
import sys

# 设置生产环境
os.environ['FLASK_ENV'] = 'production'

try:
    from waitress import serve
    from app import app
    
    print("=" * 60)
    print("🚀 BF6玩家数据统计系统 - 生产环境")
    print("=" * 60)
    print("📊 访问地址:")
    print("   本地: http://localhost:8080")
    print("   局域网: http://0.0.0.0:8080")
    print()
    print("⚠️  生产环境模式已启用")
    print("📝 日志将输出到控制台")
    print("🛑 按 Ctrl+C 停止服务")
    print("=" * 60)
    print()
    
    # 使用waitress启动
    serve(
        app,
        host='0.0.0.0',
        port=8080,
        threads=4,
        url_scheme='http',
        channel_timeout=120
    )
    
except ImportError:
    print("❌ 错误: 未安装 waitress")
    print()
    print("请运行以下命令安装:")
    print("  pip install waitress")
    sys.exit(1)
except Exception as e:
    print(f"❌ 启动失败: {e}")
    sys.exit(1)

