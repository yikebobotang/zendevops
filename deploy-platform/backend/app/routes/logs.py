from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os
from config import Config

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    try:
        # 获取部署ID
        deploy_id = request.args.get('deploy_id')
        
        if not deploy_id:
            # 返回所有日志文件列表
            log_files = [f for f in os.listdir(Config.ANSIBLE_LOGS_DIR) if f.endswith('.log')]
            logs = []
            for log_file in log_files:
                deploy_id = log_file.replace('.log', '')
                log_path = os.path.join(Config.ANSIBLE_LOGS_DIR, log_file)
                logs.append({
                    'deploy_id': deploy_id,
                    'log_file': log_file,
                    'size': os.path.getsize(log_path),
                    'created_at': os.path.getctime(log_path)
                })
            return jsonify(logs), 200
        else:
            # 返回指定部署ID的日志内容
            log_file = os.path.join(Config.ANSIBLE_LOGS_DIR, f'{deploy_id}.log')
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    content = f.read()
                return jsonify({
                    'deploy_id': deploy_id,
                    'content': content
                }), 200
            else:
                return jsonify({'message': '日志文件不存在'}), 404
                
    except Exception as e:
        return jsonify({'message': f'获取日志失败: {str(e)}'}), 500