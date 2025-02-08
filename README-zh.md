<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD041 -->

<p align="center">
    <img src="images/logo.png" alt="catenaconf logo" width=200 height=200 />
</p>
<h1 align="center">CatenaConf</h1>

<p align="center">
    <a href="https://codecov.io/github/Asianfleet/catenaconf">
        <img src="https://codecov.io/github/Asianfleet/catenaconf/graph/badge.svg?token=NK7VA3RR1G" alt="Codecov">
    </a>
    <a href="https://img.shields.io/pypi/v/catenaconf">
        <img src="https://img.shields.io/pypi/v/catenaconf" alt="Package version">
    </a>
    <a href="https://pypi.org/project/catenaconf/">
        <img src="https://img.shields.io/pypi/pyversions/catenaconf" alt="PyPI - Python Version">
    </a>
</p>
<p align="center">
    <a href="https://pypi.org/project/catenaconf/">
        <img src="https://img.shields.io/pypi/wheel/catenaconf" alt="PyPI - Format">
    </a>
    <a href="https://github.com/Asianfleet/catenaconf/actions">
        <img src="https://img.shields.io/github/actions/workflow/status/Asianfleet/catenaconf/main.yaml" alt="build passing">
    </a>
    <a href="https://opensource.org/license/apache-2-0">
        <img src="https://img.shields.io/github/license/Asianfleet/catenaconf" alt="License">
    </a>
</p>

[English](README.md) | [中文](README-zh.md)

## 简介

CatenaConf 是一个轻量级的 Python 库，用于管理和操作配置。它扩展了 Python 的字典类型，使用键值对来管理配置，并提供了灵活的操作功能。

## 特性

- 轻量级: 代码量小，可不安装任何第三方依赖（如需要从 Pydantic 模型或从 yaml 文件创建配置时则需要安装对应依赖）。
- 基于字典: 使用 Python 字典来创建和管理配置。
- 属性访问: 通过属性访问和修改配置值，方便直观。
- 灵活的更新机制: 提供灵活的更新功能，支持合并字典。
- 引用解析: 支持在配置值中引用其他配置值，并能够解析这些引用。

---

## 安装

使用 pip 安装：

```bash
pip install catenaconf
```

## 使用方法

### 创建配置

#### 从字典创建

```python
Catenaconf.create(config)
```

**描述:** 从字典创建一个 `KvConfig` 实例（库内置类型）。

**参数:**

- `config (dict)`: 包含配置数据的字典。

**返回:**

- 返回从字典创建的 `KvConfig` 对象。

**用法:**

```python
from catenaconf import Catenaconf

config = {
    "database": {
        "host": "localhost",
        "port": 3306
    }
}

cfg = Catenaconf.create(config)
```

#### 从文件加载

```python
Catenaconf.load(file)
```

**描述:** 从文件加载一个 `KvConfig` 实例。支持 JSON、YAML 和 XML 格式。

**参数:**

- `file (str | pathlib.Path)`: 配置文件的路径。

**返回:**

- 返回从加载的数据创建的 `KvConfig` 对象。

**用法:**

```python
cfg = Catenaconf.load("config.json")
```

#### 从 Pydantic 模型创建

```python
Catenaconf.structured(model)
```

**描述:** 从 Pydantic 模型创建一个 `KvConfig` 实例。

**参数:**

- `model (pydantic.BaseModel)`: 用于构造配置的 Pydantic 模型对象。

**返回:**

- 包含结构化配置的 `KvConfig` 对象。

**用法:**

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field: str
cfg = Catenaconf.structured(MyModel(field="value"))
```

### 访问配置

创建完配置后，可以通过属性方式访问配置值：

```python
from catenaconf import Catenaconf

config = {
  "database": {
    "host": "localhost",
    "port": 3306
  }
}

cfg = Catenaconf.create(config)

# 通过属性访问
host = cfg.database.host  
port = cfg.database.port

print(host)  # 输出: localhost
print(port)  # 输出: 3306
```

### 选择配置值

```python
Catenaconf.select(cfg, key, *, default="NOT FOUND", throw_on_resolution_failure=True, throw_on_missing=False)
```

**描述:** 通过键从配置中选择值，带有默认值和错误处理选项。

**参数:**

- `cfg (KvConfig)`: 要从中选择的配置实例。
- `key (str)`: 要在配置中定位的键。
- `default (Any, 可选)`: 如果未找到键时要返回的默认值。默认为 `"NOT FOUND"`。
- `throw_on_resolution_failure (bool, 可选)`: 如果键解析失败是否引发错误。默认为 `True`。
- `throw_on_missing (bool, 可选)`: 是否为缺失的键引发错误。默认为 `False`。

**返回:**

- 选定的值，或者如果未找到键则返回默认值。

**用法:**

```python
value = Catenaconf.select(cfg, "database.user", default=None, throw_on_resolution_failure=False)
```

### 更新配置

```python
Catenaconf.update(cfg, key, value=None, *, merge=True)
```

**描述:** 更新配置中指定键的值。

**参数:**

- `cfg (KvConfig)`: 要更新的配置实例。
- `key (str)`: 要更新的值的位置，以点分隔的字符串形式指定。
- `value (Any, 可选)`: 新值。
- `merge (bool, 可选)`: 是否合并字典。默认为 `True`。

**用法:**

```python
Catenaconf.update(cfg, "database.user", "root")
Catenaconf.update(cfg, "database", {"root": "root"})
Catenaconf.update(cfg, "database", {"root": "root"}, merge=True)
```

**注意事项:**

- 如果 `merge=True`，现有字典将与新值合并。

- 如果 `merge=False`，新值将替换现有值。

### 合并配置

```python
Catenaconf.merge(*configs)
```

**描述:** 将多个配置合并为一个。

**参数:**

- `*configs (KvConfig 或 dict)`: 要合并的配置，作为位置参数传递。

**返回:**

- 合并后的 `KvConfig` 实例。

**用法:**

```python
config1 = {"database": {"host": "localhost"}}
config2 = {"database": {"port": 3306}}

merged_cfg = Catenaconf.merge(config1, config2)
```

### 引用和解析引用

```python
Catenaconf.resolve(cfg)
```

**描述:** 解析配置中的所有引用。引用定义为 `@{}` 格式。

**参数:**

- `cfg (KvConfig)`: 包含引用的配置实例。

**用法:**

```python
config = {
    "info": {
        "path": "/data",
        "filename": "a.txt"
    },
    "backup_path": "@{info.path}/backup/@{info.filename}"
}

cfg = Catenaconf.create(config)
Catenaconf.resolve(cfg)
```

**注意事项:**

- 通过将占位符替换为实际值来解析引用。

### 转换为字典

```python
Catenaconf.to_container(cfg, resolve=True)
```

**描述:** 将 `KvConfig` 实例转换为标准字典。

**参数:**

- `cfg (KvConfig)`: 要转换的配置实例。
- `resolve (bool, 可选)`: 是否在字典中解析引用。默认为 `True`。

**返回:**

- 包含配置数据的标准字典。

**用法:**

```python
dict_config = Catenaconf.to_container(cfg, resolve=True)
dict_config = Catenaconf.to_container(cfg, resolve=False)
```

**注意事项:**

- 当 `resolve=True` 时，配置中的所有引用都将被解析。
- 当 `resolve=False` 时，引用保持未解析状态。
