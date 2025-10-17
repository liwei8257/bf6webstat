"""
数据处理模块
负责获取和处理玩家数据
"""

import json
import asyncio
from api_handler import TrnClient
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def load_players_config(config_file='players.json'):
    """加载玩家配置文件
    
    支持配置格式：
    - steam_usernames: Steam用户名列表（推荐）
    - players: 完整配置列表（兼容）
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 优先使用steam_usernames简化配置
        steam_usernames = config.get('steam_usernames', [])
        if steam_usernames:
            return {
                'type': 'usernames',
                'usernames': steam_usernames,
                'platform': 'steam'
            }
        
        # 兼容原有的players配置
        players = config.get('players', [])
        if players:
            return {
                'type': 'players',
                'players': players
            }
        
        return {'type': 'empty'}
        
    except FileNotFoundError:
        log.error(f"配置文件 {config_file} 未找到")
        return {'type': 'empty'}
    except json.JSONDecodeError as e:
        log.error(f"配置文件格式错误: {e}")
        return {'type': 'empty'}


async def fetch_player_stats(client: TrnClient, player_config: dict):
    """获取单个玩家的统计数据"""
    platform = player_config.get('platform', 'origin')
    user_id = player_config.get('user_id', '')
    name = player_config.get('name', user_id)
    
    log.info(f"正在获取玩家 {name} ({platform}/{user_id}) 的数据...")
    
    try:
        # 获取玩家资料
        profile = await client.player_profile(platform, user_id, fresh=True)
        
        if not profile:
            error_msg = f'无法获取数据 - 请检查玩家ID是否正确'
            if platform == 'steam':
                error_msg += ' (Steam需要使用17位数字ID)'
            log.error(f"玩家 {name}: {error_msg}")
            return {
                'name': name,
                'platform': platform,
                'user_id': user_id,
                'error': error_msg
            }
        
        # 提取关键统计数据
        segments = profile.get('segments', [])
        overview = None
        
        # 找到概览数据段
        for segment in segments:
            if segment.get('type') == 'overview':
                overview = segment
                break
        
        if not overview:
            return {
                'name': name,
                'platform': platform,
                'user_id': user_id,
                'error': '数据格式异常'
            }
        
        stats = overview.get('stats', {})
        
        
        # 提取常用统计指标
        kills = get_stat_value(stats, 'kills')
        deaths = get_stat_value(stats, 'deaths')
        kd_ratio = get_stat_value(stats, 'kdRatio') or get_stat_value(stats, 'kd') or get_stat_value(stats, 'killDeathRatio')
        
        wins = get_stat_value(stats, 'matchesWon') or get_stat_value(stats, 'wins')
        losses = get_stat_value(stats, 'matchesLost') or get_stat_value(stats, 'losses')
        win_rate = get_stat_value(stats, 'wlPercentage') or get_stat_value(stats, 'winRate')
        
        # 计算准确率：命中数 / 射击数 * 100
        shots_hit = get_stat_value(stats, 'shotsHit')
        shots_fired = get_stat_value(stats, 'shotsFired')
        accuracy = (shots_hit / shots_fired * 100) if shots_fired > 0 else 0
        
        headshots = get_stat_value(stats, 'headshotKills') or get_stat_value(stats, 'headshots')
        headshot_percentage = get_stat_value(stats, 'headshotPercentage') or get_stat_value(stats, 'headshotsPercentage')
        
        result = {
            'name': name,
            'platform': platform,
            'user_id': user_id,
            'kills': kills,
            'deaths': deaths,
            'kd_ratio': kd_ratio,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'score_per_minute': get_stat_value(stats, 'scorePerMinute') or get_stat_value(stats, 'spm'),
            'kills_per_minute': get_stat_value(stats, 'killsPerMinute') or get_stat_value(stats, 'kpm'),
            'accuracy': accuracy,
            'headshots': headshots,
            'headshot_percentage': headshot_percentage,
            'time_played': get_stat_value(stats, 'timePlayed'),
            'matches_played': get_stat_value(stats, 'matchesPlayed') or get_stat_value(stats, 'matches'),
            'revives': get_stat_value(stats, 'revives'),
            'damage': get_stat_value(stats, 'damageDealt') or get_stat_value(stats, 'damage'),
        }
        
        log.info(f"✓ 成功获取玩家 {name} 的数据 (K/D: {result['kd_ratio']})")
        return result
        
    except Exception as e:
        log.error(f"获取玩家 {name} 数据时出错: {e}")
        error_msg = str(e)
        if '400' in error_msg and platform == 'steam':
            error_msg = '玩家ID格式错误 - Steam需要使用17位数字ID，不是用户名'
        return {
            'name': name,
            'platform': platform,
            'user_id': user_id,
            'error': error_msg
        }


def get_stat_value(stats: dict, key: str, default=0):
    """从统计数据中安全获取值
    
    处理多种可能的数据格式：
    - 直接值: {"kills": 100}
    - 对象值: {"kills": {"value": 100}}
    - 显示值: {"kills": {"displayValue": "100"}}
    """
    if key not in stats:
        return default
    
    stat = stats[key]
    
    # 如果是字典，尝试多个可能的字段
    if isinstance(stat, dict):
        # 尝试 value 字段
        if 'value' in stat and stat['value'] is not None:
            return stat['value']
        # 尝试 displayValue 字段（可能需要转换）
        if 'displayValue' in stat and stat['displayValue']:
            try:
                # 移除可能的逗号和单位
                clean_value = str(stat['displayValue']).replace(',', '').split()[0]
                return float(clean_value) if '.' in clean_value else int(clean_value)
            except (ValueError, IndexError):
                pass
        return default
    
    # 直接返回值
    return stat if stat is not None else default


async def search_and_fetch_player(client: TrnClient, username: str, platform: str = 'steam'):
    """通过用户名搜索并获取玩家数据"""
    log.info(f"正在搜索玩家: {username} ({platform})...")
    
    try:
        # 先搜索玩家
        search_results = await client.search_players(platform, username)
        
        if not search_results:
            log.error(f"未找到玩家: {username}")
            return {
                'name': username,
                'platform': platform,
                'user_id': '未找到',
                'error': f'搜索不到该玩家，请检查用户名是否正确'
            }
        
        # 获取第一个匹配结果
        player_info = search_results[0]
        
        # 从搜索结果中提取正确的ID
        player_id = player_info.get('platformUserIdentifier') or player_info.get('platformUserId')
        player_name = player_info.get('platformUserHandle', username)
        
        if not player_id:
            log.error(f"无法获取玩家ID: {username}")
            return {
                'name': username,
                'platform': platform,
                'user_id': '解析失败',
                'error': '搜索结果格式异常'
            }
        
        log.info(f"找到玩家: {player_name} (ID: {player_id})")
        
        # 使用获取到的ID去查询详细数据
        player_config = {
            'name': player_name,
            'platform': platform,
            'user_id': player_id
        }
        
        return await fetch_player_stats(client, player_config)
        
    except Exception as e:
        log.error(f"搜索玩家 {username} 时出错: {e}")
        return {
            'name': username,
            'platform': platform,
            'user_id': '错误',
            'error': str(e)
        }


async def fetch_all_players_data():
    """获取所有配置玩家的数据"""
    config = load_players_config()
    
    if config['type'] == 'empty':
        log.warning("没有配置任何玩家")
        return []
    
    async with TrnClient() as client:
        results = []
        
        if config['type'] == 'usernames':
            # 通过用户名搜索模式
            usernames = config['usernames']
            platform = config['platform']
            log.info(f"开始搜索 {len(usernames)} 名玩家...")
            
            tasks = [search_and_fetch_player(client, username, platform) for username in usernames]
            results = await asyncio.gather(*tasks)
            
        elif config['type'] == 'players':
            # 传统配置模式
            players = config['players']
            log.info(f"开始获取 {len(players)} 名玩家的数据...")
            
            tasks = [fetch_player_stats(client, player) for player in players]
            results = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in results if 'error' not in r)
    log.info(f"完成！成功: {success_count}/{len(results)}")
    return results


if __name__ == '__main__':
    # 测试数据获取
    asyncio.run(fetch_all_players_data())
