<!-- markdownlint-disable MD024 -->
# Catenaconf

Catenaconf 是一个用于管理和操作配置的 Python 包。它提供了创建、更新、合并和解析配置的功能。

## 安装

使用 pip 安装：

```bash
pip install catenaconf
```

## 使用方法

### 创建配置

使用 `Catenaconf.create` 方法创建一个 `DictConfig` 实例：

```python
from catenaconf.ops import Catenaconf

config = {
    "database": {
        "host": "localhost",
        "port": 3306
    }
}

cfg = Catenaconf.create(config)
```

### 更新配置

使用 `Catenaconf.update` 方法更新配置：

```python
Catenaconf.update(cfg, "database.user", "root")
```

### 合并配置

使用 `Catenaconf.merge` 方法合并多个配置：

```python
config1 = {"database": {"host": "localhost"}}
config2 = {"database": {"port": 3306}}

merged_cfg = Catenaconf.merge(config1, config2)
```

### 解析配置

使用 `Catenaconf.resolve` 方法解析配置中的引用：

```python
config = {
    "path": "/data",
    "backup_path": "@{path}/backup"
}

cfg = Catenaconf.create(config)
Catenaconf.resolve(cfg)
```

### 转换为字典

使用 `Catenaconf.to_container` 方法将 `DictConfig` 实例转换为普通字典：

```python
dict_config = Catenaconf.to_container(cfg)
```

## Catenaconf 类功能

- `create(config: dict) -> DictConfig`: 创建一个 `DictConfig` 实例。
- `update(cfg: DictConfig, key: str, value: Any = None, *, merge: bool = True) -> None`: 更新配置，支持嵌套更新。
- `merge(*configs) -> DictConfig`: 合并多个配置，返回合并后的 `DictConfig` 实例。
- `resolve(cfg: DictConfig) -> None`: 解析配置中的引用。
- `to_container(cfg: DictConfig) -> dict`: 将 `DictConfig` 实例转换为普通字典。

## DictConfig 类特性

`DictConfig` 类是对 Python 内置 `dict` 类的扩展，增加了以下特性：

- 支持通过属性访问字典项。
- 自动将嵌套字典转换为 `DictConfig` 实例。
- 支持深拷贝。
- 支持解析引用。
- 提供方法将 `DictConfig` 实例转换为普通字典。
