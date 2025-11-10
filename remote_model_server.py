"""
远程模型存储服务示例
这是一个简单的Flask应用，演示如何实现远程模型存储服务API
"""

from flask import Flask, request, jsonify, send_file
import os
from pathlib import Path

app = Flask(__name__)

# 获取当前脚本文件的目录
CURRENT_DIR = Path(__file__).parent
BASE_MODEL_PATH = CURRENT_DIR / "models"  # 在当前目录下创建models文件夹存储模型
BASE_MODEL_PATH.mkdir(parents=True, exist_ok=True)



@app.route('/models/upload', methods=['POST'])
def upload_model():
    """上传模型文件"""
    try:
        # 获取文件
        file = request.files.get('file')
        if not file:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
            
        # 获取参数
        username = request.form.get('username')
        model_name = request.form.get('model_name')
        sub_directory = request.form.get('sub_directory', '')
        
        if not username or not model_name:
            return jsonify({'success': False, 'error': 'Missing username or model_name'}), 400
            
        # 创建用户目录
        user_path = BASE_MODEL_PATH / username
        user_path.mkdir(parents=True, exist_ok=True)
        
        # 创建子目录（如果指定）
        if sub_directory:
            target_dir = user_path / sub_directory
            target_dir.mkdir(parents=True, exist_ok=True)
        else:
            target_dir = user_path
            
        # 保存文件
        target_path = target_dir / model_name
        file.save(target_path)
        
        # 计算相对路径
        relative_path = target_path.relative_to(BASE_MODEL_PATH)
        return jsonify({
            'success': True,
            'server_path': str(relative_path),
            'message': 'File uploaded successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/models/delete', methods=['DELETE'])
def delete_model():
    """删除模型文件"""
    try:
        data = request.get_json()
        username = data.get('username')
        server_path = data.get('server_path')
        
        if not username or not server_path:
            return jsonify({'success': False, 'error': 'Missing username or server_path'}), 400
            
        # 构建文件路径
        file_path = BASE_MODEL_PATH / server_path
        
        # 确保文件在用户的目录下
        user_path = BASE_MODEL_PATH / username
        if not str(file_path).startswith(str(user_path)):
            return jsonify({'success': False, 'error': 'Access denied'}), 403
            
        # 删除文件
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            return jsonify({'success': True, 'message': 'File deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'File not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/models/download', methods=['GET', 'POST'])
def download_model():
    """下载模型文件"""
    try:
        # 根据请求方法获取数据
        if request.method == 'POST':
            data = request.get_json()
        else:
            data = request.args
            
        username = data.get('username')
        server_path = data.get('server_path')
        
        if not username or not server_path:
            return jsonify({'success': False, 'error': 'Missing username or server_path'}), 400
            
        # 构建文件路径
        file_path = BASE_MODEL_PATH / server_path
        
        # 确保文件在用户的目录下
        user_path = BASE_MODEL_PATH / username
        if not str(file_path).startswith(str(user_path)):
            return jsonify({'success': False, 'error': 'Access denied'}), 403
            
        # 检查文件是否存在
        if not file_path.exists() or not file_path.is_file():
            return jsonify({'success': False, 'error': 'File not found'}), 404
            
        # 发送文件
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/models/list', methods=['GET', 'POST'])
def list_models():
    """列出用户的所有模型文件"""
    try:
        # 根据请求方法获取数据
        if request.method == 'POST':
            data = request.get_json()
        else:
            data = request.args
            
        username = data.get('username')
        
        if not username:
            return jsonify({'success': False, 'error': 'Missing username'}), 400
            
        # 获取用户目录
        user_path = BASE_MODEL_PATH / username
        
        # 列出所有文件
        files = []
        if user_path.exists():
            for root, dirs, filenames in os.walk(user_path):
                for filename in filenames:
                    file_path = Path(root) / filename
                    relative_path = file_path.relative_to(BASE_MODEL_PATH)
                    stat = file_path.stat()
                    
                    files.append({
                        'name': filename,
                        'path': str(relative_path),
                        'size': stat.st_size,
                        'modified': stat.st_mtime
                    })
        
        return jsonify({
            'success': True,
            'files': files
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)






