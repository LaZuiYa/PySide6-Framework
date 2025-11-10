# PySide6 Framework

一个基于PySide6和PySide6-Fluent-Widgets的现代化桌面应用程序框架，集成了用户认证、权限管理、数据库支持和远程模型服务等功能。

## 功能特性

- **现代化UI界面**：基于PySide6和PySide6-Fluent-Widgets构建，提供美观流畅的用户界面
- **用户认证系统**：完整的登录认证流程
- **权限管理系统**：基于Casbin的RBAC（基于角色的访问控制）权限管理
- **多数据库支持**：支持多种数据库后端
- **SSH隧道连接**：支持通过SSH隧道连接远程数据库
- **动态路由系统**：基于菜单的动态页面路由
- **远程模型服务**：内置Flask服务器，支持远程模型存储和管理
- **依赖管理**：使用Poetry进行依赖管理

## 技术栈

- **GUI框架**：PySide6 + PySide6-Fluent-Widgets
- **数据库**：SQLAlchemy ORM
- **权限管理**：Casbin + casbin-sqlalchemy-adapter
- **SSH隧道**：sshtunnel
- **依赖管理**：Poetry
- **远程服务**：Flask

## 项目结构

```
PySide6_framework/
├── app/                    # 主应用目录
│   ├── db/                # 数据库相关
│   ├── services/          # 业务逻辑层
│   ├── ui/                # 用户界面
│   ├── config.py          # 配置文件
│   └── main.py            # 应用入口
├── remote_model_server.py # 远程模型服务
├── pyproject.toml         # 项目配置和依赖
└── poetry.toml            # Poetry配置
```

## 核心功能模块

### 1. 用户认证系统
- 登录验证
- 用户会话管理
- 密码安全存储（SHA256加密）

### 2. 权限管理系统
- 基于Casbin的RBAC权限控制
- 角色管理（创建、删除、编辑）
- 用户角色分配
- 菜单权限控制

### 3. 菜单管理系统
- 动态菜单树
- 多级菜单支持
- 菜单图标选择
- 菜单与页面路由绑定

### 4. 数据库支持
- 多种数据库支持（MySQL、PostgreSQL等）
- SSH隧道连接远程数据库
- 数据库连接池管理

### 5. 远程模型服务
- 模型文件上传/下载
- 模型文件管理
- 用户隔离的模型存储

## 安装与配置

### 环境要求
- Python 3.9 - 3.12
- Poetry（依赖管理）
## 安装Poetry
### 1. 安装 pipx (如果还没有)
```bash
pip install pipx
pipx ensurepath
```
### 2. 使用 pipx 安装 poetry
```bash
pipx install poetry
```
### 3. 验证安装
```bash
poetry --version
```
你应该会看到类似 "Poetry (version 1.8.3)" 的输出
### 安装步骤

请根据你的环境选择**一种**设置方式：

### 方案 A: (推荐) 使用 Conda + Poetry

(推荐给需要 Conda 管理 Python 解释器和底层库的开发者)

1.  **克隆项目**
    ```bash
    git clone https://github.com/LaZuiYa/PySide6-Framework.git
    cd py-side6-framework
    ```

2.  **创建并激活 Conda 环境**
    (请使用 `pyproject.toml` 中指定的 Python 版本)
    ```bash
    conda create -n my_project_env python=3.9
    conda activate my_project_env
    ```

3.  **配置 Poetry 使用当前环境**
    (这一步是告诉 Poetry："请使用我激活的 Conda 环境，不要自己创建 .venv")
    ```bash
    poetry config virtualenvs.create false --local
    ```

4.  **安装所有依赖**
    (Poetry 会读取 `poetry.lock` 文件，并将所有包安装到 `my_project_env` 中)
    ```bash
    poetry install
    ```

### 方案 B: (标准) 仅使用 Poetry

(适用于不使用 Conda 的开发者)

1.  **克隆项目**
    ```bash
    git clone https://github.com/LaZuiYa/PySide6-Framework.git
    cd py-side6-framework
    ```

2.  **安装所有依赖**
    (Poetry 会自动检测 `pyproject.toml`，创建一个新的 `.venv` 虚拟环境，并根据 `poetry.lock` 安装所有包)
    ```bash
    poetry install
    ```



### 配置数据库连接：
编辑`app/config.py`文件，修改数据库连接参数：
```python
# SSH服务器信息
SSH_HOST = 'xxx.xxx.xxx.xxx'
SSH_PORT = 22
SSH_USER = 'your_ssh_user'
SSH_PASSWORD = 'your_ssh_password'

# 数据库信息
DB_USER = 'your_db_user'
DB_PASSWORD = 'your_db_password'
DB_NAME = 'your_db_name'
DB_REMOTE_HOST = '127.0.0.1'
DB_REMOTE_PORT = 3306
```

### 启动应用

1. 启动主应用：
```bash
poetry run python -m app.main
```

2. 启动远程模型服务（可选）：
```bash
poetry run python remote_model_server.py
```

## 使用说明

### 默认账户
系统默认提供admin账户，初始密码为`admin123`。

### 系统管理功能
登录后可在"系统管理"菜单中访问以下功能：
1. **用户管理**：创建、删除用户，重置密码
2. **菜单管理**：创建、编辑、删除菜单项
3. **权限管理**：角色管理，用户角色分配，权限设置

### 权限控制
- 基于Casbin的RBAC模型
- 支持用户直接授权和角色继承授权
- 菜单级别的细粒度权限控制

## 开发指南

### 添加新页面
1. 在`app/ui/pages/`目录下创建新页面文件
2. 页面类名需遵循命名规范（如：`systemUserPage.py`对应`SystemUserPage`类）
3. 在菜单管理中添加对应菜单项和路由

### 数据库模型
数据库模型定义在`app/db/models.py`中，包含：
- User（用户）
- Menu（菜单）
- Model（模型）

### 服务层
业务逻辑实现在`app/services/`目录中，包括：
- 认证服务
- 用户管理服务
- 菜单管理服务
- 权限管理服务


## 📦 依赖管理 (重要!)

**请不要**使用 `pip install` 或 `conda install` 来添加 Python 包，这会破坏 `poetry.lock` 带来的一致性。

* **添加一个新的"生产"依赖** (例如 `requests`)
    ```bash
    poetry add requests
    ```

* **添加一个新的"开发"依赖** (例如 linter `ruff`)
    ```bash
    poetry add ruff --group dev
    ```

* **移除一个依赖**
    ```bash
    poetry remove requests
    ```

* **更新一个依赖**
    ```bash
    poetry update requests
    ```

**重要：** 在 `add/remove/update` 依赖后，`pyproject.toml` 和 `poetry.lock` 文件会发生变化。**请务必将这两个文件提交到 Git**，以便团队其他成员可以同步。

* **同步团队的依赖更新** (当你拉取了新的 `poetry.lock` 文件后)
    ```bash
    poetry install
    ```
  
## 许可证

本项目仅供学习和参考使用。

## 贡献

欢迎提交Issue和Pull Request来改进这个框架。
