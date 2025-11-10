import casbin
from casbin_sqlalchemy_adapter import Adapter
from app.config import get_db_engine
import os

# Casbin model 写入同目录 .conf
RBAC_MODEL_TEXT = """
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

g = _, _
# 可以扩展g2, g3用于更多关联

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
"""

MODEL_PATH = os.path.join(os.path.dirname(__file__), "rbac_model.conf")
if not os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "w", encoding="utf8") as f:
        f.write(RBAC_MODEL_TEXT)

# 延迟初始化 Casbin 适配器和执行器
adapter = None
enforcer = None

def init_enforcer():
    """初始化 Casbin 适配器和执行器"""
    global adapter, enforcer
    if adapter is None or enforcer is None:
        # 获取数据库引擎（这将建立SSH隧道和数据库连接）
        engine = get_db_engine()
        adapter = Adapter(engine)
        enforcer = casbin.Enforcer(MODEL_PATH, adapter)
    return enforcer

def get_enforcer():
    """获取 Casbin 执行器实例"""
    if enforcer is None:
        init_enforcer()
    return enforcer

def reload_enforcer():
    """重新加载策略"""
    if enforcer is None:
        init_enforcer()
    enforcer.load_policy()