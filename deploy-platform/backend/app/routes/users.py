from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import bcrypt
import uuid

# 模拟用户数据存储
users_db = {
    'admin': {
        'id': '1',
        'username': 'admin',
        'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()),
        'role': 'admin',
        'email': 'admin@example.com',
        'created_at': '2025-12-02T10:00:00Z'
    }
}

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """获取用户列表"""
    users_list = []
    for user in users_db.values():
        # 不返回密码
        user_info = {
            'id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'email': user['email'],
            'created_at': user['created_at']
        }
        users_list.append(user_info)
    return jsonify(users_list), 200

@users_bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """获取单个用户信息"""
    for user in users_db.values():
        if user['id'] == user_id:
            user_info = {
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'email': user['email'],
                'created_at': user['created_at']
            }
            return jsonify(user_info), 200
    return jsonify({'message': '用户不存在'}), 404

@users_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    """创建新用户"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    email = data.get('email')
    
    if not username or not password or not email:
        return jsonify({'message': '用户名、密码和邮箱不能为空'}), 400
    
    if username in users_db:
        return jsonify({'message': '用户名已存在'}), 400
    
    # 创建新用户
    user_id = str(uuid.uuid4())
    users_db[username] = {
        'id': user_id,
        'username': username,
        'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
        'role': role,
        'email': email,
        'created_at': '2025-12-02T10:00:00Z'  # 实际项目中应使用当前时间
    }
    
    return jsonify({
        'message': '用户创建成功',
        'user_id': user_id
    }), 201

@users_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """更新用户信息"""
    data = request.get_json()
    
    # 查找用户
    user_to_update = None
    username_key = None
    for username, user in users_db.items():
        if user['id'] == user_id:
            user_to_update = user
            username_key = username
            break
    
    if not user_to_update:
        return jsonify({'message': '用户不存在'}), 404
    
    # 更新用户信息
    if 'password' in data:
        user_to_update['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    if 'role' in data:
        user_to_update['role'] = data['role']
    if 'email' in data:
        user_to_update['email'] = data['email']
    
    users_db[username_key] = user_to_update
    
    return jsonify({'message': '用户信息更新成功'}), 200

@users_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """删除用户"""
    # 查找用户
    username_to_delete = None
    for username, user in users_db.items():
        if user['id'] == user_id:
            username_to_delete = username
            break
    
    if not username_to_delete:
        return jsonify({'message': '用户不存在'}), 404
    
    # 不能删除admin用户
    if username_to_delete == 'admin':
        return jsonify({'message': '不能删除管理员用户'}), 400
    
    del users_db[username_to_delete]
    
    return jsonify({'message': '用户删除成功'}), 200