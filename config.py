"""
应用配置文件
支持开发环境和生产环境
"""
import os

class Config:
    """基础配置"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'bf6-stats-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 生产环境SECRET_KEY，如果未设置则使用默认值
    SECRET_KEY = os.getenv('SECRET_KEY', 'bf6-stats-default-secret-key-change-me')

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

