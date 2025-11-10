import os
import urllib
from dataclasses import dataclass
from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder
import sqlalchemy

load_dotenv()

# --- 服务器凭据配置 ---

# SSH服务器信息
SSH_HOST = 'xxx.xxx.xxx.xxx'
SSH_PORT = 22
SSH_USER = 'devUser'
SSH_PASSWORD = 'xxx'

# MySQL数据库信息
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'pyside6_framework'
DB_REMOTE_HOST = '127.0.0.1'
DB_REMOTE_PORT = 3306

# 远程模型服务器信息
MODEL_SERVER_URL = os.getenv('MODEL_SERVER_URL', 'http://127.0.0.1:8000')
use_ssh = False
@dataclass
class AppConfig:
    db_url: str = None
    env: str = os.getenv("APP_ENV", "dev")
    app_title: str = os.getenv("APP_TITLE", "PySide6 Framework")
    model_server_url: str = MODEL_SERVER_URL
    engine: sqlalchemy.Engine = None
    tunnel: SSHTunnelForwarder = None

config = AppConfig()

def init_config():
    """初始化配置，建立SSH隧道和数据库连接"""
    global config
    if use_ssh:
    
        try:
            # 建立SSH隧道
            tunnel = SSHTunnelForwarder(
                (SSH_HOST, SSH_PORT),
                ssh_username=SSH_USER,
                ssh_password=SSH_PASSWORD,
                remote_bind_address=(DB_REMOTE_HOST, DB_REMOTE_PORT),
                local_bind_address=('127.0.0.1', 0)  # 自动选择本地端口
            )

            tunnel.start()
            config.tunnel = tunnel

            # 获取自动分配的本地端口
            local_port = tunnel.local_bind_port

            # URL编码密码
            encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

            # 构造数据库URL
            config.db_url = (
                f"mysql+pymysql://{DB_USER}:{encoded_password}"
                f"@127.0.0.1:{local_port}/{DB_NAME}"
            )

            # 创建数据库引擎
            config.engine = sqlalchemy.create_engine(config.db_url)

        except Exception as e:
            print(f"配置初始化失败: {e}")
            if hasattr(config, 'tunnel') and config.tunnel:
                config.tunnel.stop()
            raise
    else:
        try:
            # URL编码密码
            encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

            # 构造数据库URL（假设MySQL运行在本地默认端口）
            config.db_url = (
                f"mysql+pymysql://{DB_USER}:{encoded_password}"
                f"@127.0.0.1:{DB_REMOTE_PORT}/{DB_NAME}"
            )

            # 创建数据库引擎
            config.engine = sqlalchemy.create_engine(config.db_url)

        except Exception as e:
            print(f"配置初始化失败: {e}")
            raise

def get_db_engine():
    """获取数据库引擎实例"""
    if not config.engine:
        init_config()
    return config.engine

def close_tunnel():
    """关闭SSH隧道"""
    if config.tunnel and config.tunnel.is_active:
        config.tunnel.stop()



