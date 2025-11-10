from __future__ import annotations

from typing import List

from sqlalchemy import select
from app.db.base import Base, engine, session_scope
from app.db.models import User,  Menu
from app.services.auth import hash_password
from app.services.casbin_enforcer import get_enforcer, reload_enforcer

def init_db() -> None:
    # 初始化数据库连接
    from app.db.base import init_database
    db_engine = init_database()
    Base.metadata.create_all(bind=db_engine)
    # # 创建初始数据
    # seed_admin()


# def seed_admin() -> None:
    # with session_scope() as s:
    #     # 角色
    #     admin_role = s.scalar(select(Role).where(Role.name == "admin"))
    #     if admin_role is None:
    #         admin_role = Role(name="admin", description="超级管理员")
    #         s.add(admin_role)
    #         s.flush()

    #     # 权限占位
    #     perm_codes: List[str] = [
    #         "user.manage",
    #         "menu.manage",
    #         "role.manage",
    #         "permission.manage",
    #     ]
    #     for code in perm_codes:
    #         perm = s.scalar(select(Permission).where(Permission.code == code))
    #         if perm is None:
    #             s.add(Permission(code=code, description=code))
    #     s.flush()

    #     # 管理员账号
    #     admin_user = s.scalar(select(User).where(User.username == "admin"))
    #     if admin_user is None:
    #         admin_user = User(
    #             username="admin",
    #             password_hash=hash_password("admin123"),
    #             is_active=True,
    #         )
    #         s.add(admin_user)
    #         s.flush()
    #     if admin_role not in admin_user.roles:
    #         admin_user.roles.append(admin_role)

    #     # 菜单
    #     def ensure_menu(name: str, route_key: str, icon: str | None, parent: Menu | None = None) -> Menu:
    #         m = s.scalar(select(Menu).where(Menu.route_key == route_key))
    #         if m is None:
    #             m = Menu(name=name, route_key=route_key, icon=icon, parent=parent)
    #             s.add(m)
    #             s.flush()
    #         return m

    #     home = ensure_menu("主页", "home", "HOME")
    #     sys_mgr = ensure_menu("系统管理", "system", "SETTINGS")
    #     comp_mgr = ensure_menu("构件管理", "component", "FOLDER")
    #     algo_mgr = ensure_menu("算法管理", "algorithm", "ROCKET")
    #     model_mgr = ensure_menu("模型管理", "model", "BRAIN")

    #     ensure_menu("用户管理", "system/users", "CONTACT", sys_mgr)
    #     ensure_menu("菜单管理", "system/menus", "LIST", sys_mgr)
    #     ensure_menu("权限管理", "system/permissions", "SECURITY", sys_mgr)

    #     # 赋菜单给管理员角色
    #     for m in [home, sys_mgr, comp_mgr, algo_mgr, model_mgr]:
    #         if m not in admin_role.menus:
    #             admin_role.menus.append(m)

    # # 用casbin授权admin角色与admin账号获得所有菜单view权限
    # e = get_enforcer()
    # e.clear_policy()
    # reload_enforcer()
    # # 载入所有菜单
    # with session_scope() as s:
    #     menus = s.query(Menu).all()
    #     # admin账号直接view全部菜单
    #     for m in menus:
    #         e.add_permission_for_user("admin", m.route_key, "view")
    #     # admin角色也view全部菜单
    #     for m in menus:
    #         e.add_permission_for_user("admin", m.route_key, "view")
    #     # admin账号加入admin角色组
    #     e.add_role_for_user("admin", "admin")
    # e.save_policy()
