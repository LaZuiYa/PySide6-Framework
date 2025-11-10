from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import Model, User
from app.services.modelStorageService import model_storage_service


def list_user_models(session: Session, user_id: int) -> List[Model]:
    """列出用户的所有模型"""
    return session.query(Model).filter(Model.owner_id == user_id).all()


def list_public_models(session: Session) -> List[Model]:
    """列出所有公开的模型"""
    return session.query(Model).filter(Model.is_public == True).all()


def get_model_by_id(session: Session, model_id: int) -> Optional[Model]:
    """根据ID获取模型"""
    return session.get(Model, model_id)


def create_model(session: Session, name: str, owner_id: int, file_path: str, 
                 file_size: int = 0, description: str = None, is_public: bool = False) -> Model:
    """创建新模型记录"""
    model = Model(
        name=name,
        owner_id=owner_id,
        file_path=file_path,
        file_size=file_size,
        description=description,
        is_public=is_public
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


def update_model(session: Session, model_id: int, **kwargs) -> Optional[Model]:
    """更新模型信息"""
    model = session.get(Model, model_id)
    if not model:
        return None
    
    for key, value in kwargs.items():
        if hasattr(model, key):
            setattr(model, key, value)
    
    session.commit()
    session.refresh(model)
    return model


def delete_model(session: Session, model_id: int) -> bool:
    """删除模型"""
    model = session.get(Model, model_id)
    if not model:
        return False
    
    # 同时删除服务器上的文件
    from app.db.base import session_scope
    with session_scope() as user_session:
        user = user_session.get(User, model.owner_id)
        if user:
            try:
                model_storage_service.delete_model_file(user, model.file_path)
            except Exception as e:
                print(f"Warning: Failed to delete model file from remote server: {e}")
    
    session.delete(model)
    session.commit()
    return True


def toggle_model_visibility(session: Session, model_id: int) -> Optional[bool]:
    """切换模型可见性"""
    model = session.get(Model, model_id)
    if not model:
        return None
    
    model.is_public = not model.is_public
    session.commit()
    session.refresh(model)
    return model.is_public


def save_trained_model(session: Session, user: User, model_name: str, model_data: bytes, 
                      sub_directory: str = "", description: str = None) -> Optional[Model]:
    """
    保存训练好的模型
    
    Args:
        session: 数据库会话
        user: 用户对象
        model_name: 模型名称
        model_data: 模型数据
        sub_directory: 子目录
        description: 模型描述
        
    Returns:
        Model对象或None
    """
    # 保存到远程服务器
    success, server_path, error = model_storage_service.save_model_file(
        user, model_name, model_data, sub_directory)
    
    if not success:
        raise Exception(f"保存模型文件失败: {error}")
        
    # 创建数据库记录
    model = create_model(
        session=session,
        name=model_name,
        owner_id=user.id,
        file_path=server_path,
        file_size=len(model_data),
        description=description
    )
    
    return model


def upload_model_file(session: Session, user: User, local_file_path: str,
                     model_name: str = None, sub_directory: str = "", 
                     description: str = None) -> Optional[Model]:
    """
    上传模型文件
    
    Args:
        session: 数据库会话
        user: 用户对象
        local_file_path: 本地文件路径
        model_name: 模型名称
        sub_directory: 子目录
        description: 模型描述
        
    Returns:
        Model对象或None
    """
    # 上传到远程服务器
    success, server_path, error = model_storage_service.upload_model_file(
        user, local_file_path, model_name, sub_directory)

    if not success:
        print(error)
        raise Exception(f"上传模型文件失败: {error}")
        
    # 获取文件大小
    import os
    file_size = os.path.getsize(local_file_path)
    
    # 确定模型名称
    if model_name is None:
        model_name = os.path.basename(local_file_path)
        
    # 创建数据库记录
    model = create_model(
        session=session,
        name=model_name,
        owner_id=user.id,
        file_path=server_path,
        file_size=file_size,
        description=description
    )
    
    return model


def download_model_file(session: Session, user: User, model_id: int, local_file_path: str) -> bool:
    """
    下载模型文件
    
    Args:
        session: 数据库会话
        user: 用户对象
        model_id: 模型ID
        local_file_path: 本地保存路径
        
    Returns:
        是否下载成功
    """
    model = session.get(Model, model_id)
    if not model:
        return False
        
    try:
        return model_storage_service.download_model_file(user, model.file_path, local_file_path)
    except Exception as e:
        print(f"Warning: Failed to download model file: {e}")
        return False