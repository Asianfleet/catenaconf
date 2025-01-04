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
