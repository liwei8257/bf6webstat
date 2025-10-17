"""
导出玩家数据到静态JSON文件
本地运行后推送到GitHub，Render读取静态文件
"""
import asyncio
import json
import time
from data_processor import fetch_all_players_data

async def export():
    print("正在获取玩家数据...")
    data = await fetch_all_players_data()
    
    result = {
        'timestamp': int(time.time()),
        'update_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'data': data,
        'success_count': sum(1 for d in data if 'error' not in d)
    }
    
    with open('static/players_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已导出！")
    print(f"   成功: {result['success_count']}/{len(data)}")
    print(f"   文件: static/players_data.json")
    print(f"   时间: {result['update_time']}")
    print()
    print("下一步：推送到GitHub")
    print("  git add static/players_data.json")
    print("  git commit -m 'Update player data'")
    print("  git push")

if __name__ == '__main__':
    asyncio.run(export())

