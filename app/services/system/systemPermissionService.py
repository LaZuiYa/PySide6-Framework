from __future__ import annotations
from typing import List
from app.services.casbin_enforcer import get_enforcer

# roles = list from all g where v1 可用，users同理
def list_roles() -> List[str]:
    e = get_enforcer()
    # 从p策略组中获取所有角色（p策略的第一个元素是角色或用户）
    roles = set()

    # 获取所有p策略
    policies = e.get_policy()
    for policy in policies:
        if len(policy) >= 3:
            # 第一个元素是主体（可能是角色或用户）
            subject = policy[0]

            roles.add(subject)  # p[1] 是角色名

    return sorted(roles)


def list_users() -> List[str]:
    e = get_enforcer()
    return sorted({p[0] for p in e.get_named_grouping_policy("g") if p[0]})

# 添加创建角色函数
def create_role(role: str) -> bool:
    """
    创建一个新角色（通过给角色分配一个临时权限来创建角色）
    """
    e = get_enforcer()
    # 添加一个占位权限来创建角色
    e.add_policy(role, "home", "view")

    e.save_policy()
    return True

# 添加删除角色函数
def delete_role(role: str) -> bool:
    """
    删除角色及其所有关联权限和用户关系
    """
    e = get_enforcer()
    # 删除角色的所有权限
    e.delete_permissions_for_user(role)
    # 删除分配给用户的角色
    e.delete_roles_for_user(role)
    # 删除角色继承关系
    e.delete_user(role)
    e.save_policy()
    return True

# 用户与角色

def assign_role_to_user(user: str, role: str) -> bool:
    e = get_enforcer()
    changed = e.add_role_for_user(user, role)
    e.save_policy()
    return changed

def remove_role_from_user(user: str, role: str) -> bool:
    e = get_enforcer()
    changed = e.delete_role_for_user(user, role)
    e.save_policy()
    return changed

def get_user_roles(user: str) -> List[str]:
    e = get_enforcer()
    return e.get_roles_for_user(user)

# 用户权限P

def assign_permission_to_user(user: str, menu: str, act: str = "view") -> bool:
    e = get_enforcer()
    changed = e.add_permission_for_user(user, menu, act)
    e.save_policy()
    return changed

def remove_permission_from_user(user: str, menu: str, act: str = "view") -> bool:
    e = get_enforcer()
    changed = e.delete_permission_for_user(user, menu, act)
    e.save_policy()
    return changed

def get_user_permissions(user: str) -> List[tuple]:
    e = get_enforcer()
    # 包括直授的
    return [p for p in e.get_permissions_for_user(user)]

# 角色权限P

def assign_permission_to_role(role: str, menu: str, act: str = "view") -> bool:
    e = get_enforcer()
    changed = e.add_permission_for_user(role, menu, act)
    e.save_policy()
    return changed

def remove_permission_from_role(role: str, menu: str, act: str = "view") -> bool:
    e = get_enforcer()
    changed = e.delete_permission_for_user(role, menu, act)
    e.save_policy()
    return changed

def get_role_permissions(role: str) -> List[tuple]:
    e = get_enforcer()
    return [p for p in e.get_permissions_for_user(role)]

# 设置角色权限（先清除后设置）
def set_role_permissions(role: str, permissions: List[tuple]) -> bool:
    """
    设置角色权限（会先清空角色的所有权限）
    :param role: 角色名
    :param permissions: 权限列表，格式 [(menu, act), ...]
    """
    e = get_enforcer()
    # 先删除所有权限
    e.delete_permissions_for_user(role)
    # 添加新权限
    for perm in permissions:
        if len(perm) >= 2:
            e.add_permission_for_user(role, perm[0], perm[1] if len(perm) > 2 else "view")
    e.save_policy()
    return True

# 设置用户角色（先清除后设置）
def set_user_roles(user: str, roles: List[str]) -> bool:
    """
    设置用户角色（会先清空用户的所有角色）
    :param user: 用户名
    :param roles: 角色列表
    """
    e = get_enforcer()
    # 先删除所有角色
    e.delete_roles_for_user(user)
    # 添加新角色
    for role in roles:
        e.add_role_for_user(user, role)
    e.save_policy()
    return True

# 查询用户所有菜单权限(直授+来自角色)
def get_user_all_menu_permissions(user: str) -> List[str]:
    e = get_enforcer()
    # v[1]: menu key
    ret = set()
    # 直授
    for p in e.get_permissions_for_user(user):
        if len(p) >= 3 and p[2]=="view":
            ret.add(p[1])
    # 来自角色
    for role in e.get_roles_for_user(user):
        for p in e.get_permissions_for_user(role):
            if len(p) >=3 and p[2]=="view":
                ret.add(p[1])
    return sorted(ret)