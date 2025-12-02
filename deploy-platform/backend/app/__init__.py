from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from app.routes.auth import auth_bp
from app.routes.deploy import deploy_bp
from app.routes.logs import logs_bp
from app.routes.users import users_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化JWT
    jwt = JWTManager(app)
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(deploy_bp, url_prefix='/api')
    app.register_blueprint(logs_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    
    return app