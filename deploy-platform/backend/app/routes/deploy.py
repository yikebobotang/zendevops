from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os
import uuid
from config import Config

deploy_bp = Blueprint('deploy', __name__)

@deploy_bp.route('/deploy', methods=['POST'])
@jwt_required()
def deploy_service():
    data = request.get_json()
    service_type = data.get('service_type')
    config = data.get('config', {})
    
    if not service_type:
        return jsonify({'message': '服务类型不能为空'}), 400
    
    # 生成唯一部署ID
    deploy_id = str(uuid.uuid4())
    
    # 模拟部署（实际项目中应调用Ansible）
    try:
        # 这里可以根据service_type选择不同的playbook
        playbook_path = os.path.join(Config.ANSIBLE_PLAYBOOKS_DIR, f'{service_type}.yml')
        
        # 记录部署日志
        log_file = os.path.join(Config.ANSIBLE_LOGS_DIR, f'{deploy_id}.log')
        
        # 模拟部署过程
        with open(log_file, 'w') as f:
            f.write(f"部署服务: {service_type}\n")
            f.write(f"部署配置: {config}\n")
            f.write("部署开始...\n")
            f.write("部署中...\n")
            f.write("部署完成!\n")
        
        return jsonify({
            'message': '部署任务已提交',
            'deploy_id': deploy_id,
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'部署失败: {str(e)}'}), 500

@deploy_bp.route('/services', methods=['GET'])
@jwt_required()
def get_services():
    # 模拟返回支持的服务列表
    services = [
        {'name': 'mysql', 'display_name': 'MySQL', 'default_port': 3306},
        {'name': 'redis', 'display_name': 'Redis', 'default_port': 6379},
        {'name': 'zookeeper', 'display_name': 'ZooKeeper', 'default_port': 2181}
    ]
    return jsonify(services), 200