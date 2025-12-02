from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt

# 模拟用户数据（实际项目中应使用数据库）
users = {
    'admin': {
        'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()),
        'role': 'admin'
    }
}

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空'}), 400
    
    user = users.get(username)
    if not user:
        return jsonify({'message': '用户名或密码错误'}), 401
    
    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        access_token = create_access_token(identity={'username': username, 'role': user['role']})
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({'message': '用户名或密码错误'}), 401