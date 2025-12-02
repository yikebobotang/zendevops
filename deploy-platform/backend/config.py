import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时
    
    # Ansible配置
    ANSIBLE_PLAYBOOKS_DIR = os.path.join(os.path.dirname(__file__), 'ansible_playbooks')
    ANSIBLE_LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'app.log')