from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import Menu
from app.services.system.systemPermissionService import assign_permission_to_role

def list_menus(session: Session) -> List[Menu]:
    return session.query(Menu).all()

def create_menu(session: Session, name: str, route_key: str, icon: str = None, parent_id: int = None) -> Menu:
    m = Menu(name=name, route_key=route_key, icon=icon, parent_id=parent_id)
    session.add(m)
    session.commit()
    
    # 创建菜单后，默认给admin角色分配查看权限
    try:
        assign_permission_to_role("admin", route_key, "view")
    except Exception as e:
        # 如果分配权限失败，不回滚菜单创建操作
        print(f"Warning: Failed to assign permission to admin role: {e}")
    
    return m

def update_menu(session: Session, menu_id: int, name: Optional[str]=None, route_key: Optional[str]=None, icon: Optional[str]=None, parent_id: Optional[int]=None) -> Optional[Menu]:
    m = session.get(Menu, menu_id)
    if not m:
        return None
    if name is not None:
        m.name = name
    if route_key is not None:
        m.route_key = route_key
    if icon is not None:
        m.icon = icon
    if parent_id is not None:
        m.parent_id = parent_id
    session.commit()
    return m

def delete_menu(session: Session, route_key: str) -> bool:
    m = session.query(Menu).filter(Menu.route_key == route_key).scalar()
    if not m:
        return False
    
    # 删除与该菜单相关的所有权限记录
    from app.services.casbin_enforcer import get_enforcer
    e = get_enforcer()
    
    # 删除角色权限 (p, role, menu, act)
    policies_to_remove = []
    for policy in e.get_policy():
        if len(policy) >= 3 and policy[1] == m.route_key:
            policies_to_remove.append(policy)
    
    # 删除用户直授权限 (p, user, menu, act) 
    for policy in e.get_policy():
        if len(policy) >= 3 and policy[1] == m.route_key:
            policies_to_remove.append(policy)
    
    # 执行删除
    for policy in policies_to_remove:
        e.remove_policy(*policy)
    
    e.save_policy()
    
    # 删除菜单本身
    session.delete(m)
    session.commit()
    return True

# 递归生成菜单树
def menu_tree(session: Session, parent_id: int = None):
    menus = session.query(Menu).filter(Menu.parent_id == parent_id).all()
    def build_node(menu: Menu):
        return {
            "id": menu.id,
            "name": menu.name,
            "route_key": menu.route_key,
            "icon": menu.icon,
            "children": menu_tree(session, menu.id),
            "updated_at": menu.updated_at
        }
    return [build_node(m) for m in menus]