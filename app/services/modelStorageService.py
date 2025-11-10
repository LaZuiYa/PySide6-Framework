from __future__ import annotations
import os
import requests
from pathlib import Path
from typing import Optional, Tuple
from app.db.models import User
from app.config import config
import json


class RemoteModelStorageService:
    """
    远程模型存储服务，处理模型文件在远程服务器上的存储
    """
    
    def __init__(self):
        """
        初始化远程模型存储服务
        """
        self.remote_server_url = config.model_server_url.rstrip('/')
        
    def save_model_file(self, user: User, model_name: str, model_data: bytes, 
                       sub_directory: str = "") -> Tuple[bool, str, str]:
        """
        保存模型文件到远程服务器
        
        Args:
            user: 用户对象
            model_name: 模型名称
            model_data: 模型数据
            sub_directory: 子目录（可选）
            
        Returns:
            Tuple[是否成功, 服务器路径, 错误信息]
        """
        try:
            # 构建请求数据
            files = {'file': (model_name, model_data)}
            data = {
                'username': user.username,
                'model_name': model_name,
                'sub_directory': sub_directory
            }
            
            # 发送POST请求到远程服务器
            response = requests.post(
                f"{self.remote_server_url}/models/upload",
                files=files,
                data=data,
                timeout=300  # 5分钟超时
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    return True, result.get('server_path', ''), ""
                else:
                    return False, "", result.get('error', 'Unknown error')
            else:
                return False, "", f"HTTP {response.status_code}: {response.text}"
        except Exception as e:
            return False, "", str(e)
            
    def upload_model_file(self, user: User, local_file_path: str, 
                         model_name: str = None, sub_directory: str = "") -> Tuple[bool, str, str]:
        """
        上传本地模型文件到远程服务器
        
        Args:
            user: 用户对象
            local_file_path: 本地文件路径
            model_name: 模型名称（可选，默认使用文件名）
            sub_directory: 子目录（可选）
            
        Returns:
            Tuple[是否成功, 服务器路径, 错误信息]
        """
        try:
            if not os.path.exists(local_file_path):
                return False, "", "本地文件不存在"
                
            if model_name is None:
                model_name = os.path.basename(local_file_path)
                
            # 发送文件到远程服务器
            with open(local_file_path, 'rb') as f:
                files = {'file': (model_name, f)}
                data = {
                    'username': user.username,
                    'model_name': model_name,
                    'sub_directory': sub_directory
                }
                
                response = requests.post(
                    f"{self.remote_server_url}/models/upload",
                    files=files,
                    data=data,
                    timeout=300  # 5分钟超时
                )
                
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    return True, result.get('server_path', ''), ""
                else:
                    return False, "", result.get('error', 'Unknown error')
            else:
                return False, "", f"HTTP {response.status_code}: {response.text}"
        except Exception as e:
            return False, "", str(e)
            
    def delete_model_file(self, user: User, server_relative_path: str) -> bool:
        """
        删除远程服务器上的模型文件
        
        Args:
            user: 用户对象
            server_relative_path: 服务器上的相对路径
            
        Returns:
            是否删除成功
        """
        try:
            # 发送删除请求到远程服务器
            response = requests.delete(
                f"{self.remote_server_url}/models/delete",
                json={
                    'username': user.username,
                    'server_path': server_relative_path
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False)
            return False
        except Exception:
            return False
            
    def download_model_file(self, user: User, server_relative_path: str, 
                           local_file_path: str) -> bool:
        """
        从远程服务器下载模型文件
        
        Args:
            user: 用户对象
            server_relative_path: 服务器上的相对路径
            local_file_path: 本地保存路径
            
        Returns:
            是否下载成功
        """
        try:
            # 发送下载请求到远程服务器
            response = requests.post(
                f"{self.remote_server_url}/models/download",
                json={
                    'username': user.username,
                    'server_path': server_relative_path
                },
                timeout=300  # 5分钟超时
            )
            
            if response.status_code == 200:
                # 保存文件到本地
                with open(local_file_path, 'wb') as f:
                    f.write(response.content)
                return True
            return False
        except Exception:
            return False
            
    def list_user_files(self, user: User) -> list:
        """
        列出用户的所有模型文件
        
        Args:
            user: 用户对象
            
        Returns:
            文件列表
        """
        try:
            # 发送请求到远程服务器获取文件列表
            response = requests.post(
                f"{self.remote_server_url}/models/list",
                json={'username': user.username},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    return result.get('files', [])
            return []
        except Exception:
            return []


# 全局实例
model_storage_service = RemoteModelStorageService()