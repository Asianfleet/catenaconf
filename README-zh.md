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
    <a href="https://badge.fury.io/py/pyecharts">
        <img src="https://badge.fury.io/py/pyecharts.svg" alt="Package version">
    </a>
    <a href="https://pypi.org/project/pyecharts/">
        <img src="https://img.shields.io/pypi/pyversions/pyecharts.svg?colorB=brightgreen" alt="PyPI - Python Version">
    </a>
</p>
<p align="center">
    <a href="https://pypi.org/project/pyecharts">
        <img src="https://img.shields.io/pypi/format/pyecharts.svg" alt="PyPI - Format">
    </a>
     <a href="https://github.com/pyecharts/pyecharts/pulls">
        <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat" alt="Contributions welcome">
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="License">
    </a>
</p>

## 简介

CatenaConf 是一个轻量级的 Python 库，专为管理和操作配置而设计。它扩展了 Python 字典类型，使用键值对管理配置，并提供灵活的操作功能。

## 特性

- 轻量级：仅依赖于 Python 标准库，无需任何第三方依赖。
- 基于 Python 字典来创建配置。
- 可以通过属性访问和修改配置值。
- 提供灵活的更新与合并机制。
- 支持在配置值中引用其他配置值。

---

## 安装

通过 pip 安装：

```bash
pip install catenaconf
```

## 使用方法

### 创建配置

#### 从字典创建

```python
Catenaconf.create(config)
```

**描述：** 从字典创建一个 `KvConfig` 实例（库内置类型之一）。

**参数：**

- `config (dict)`：包含配置数据的字典。

**用法：**

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

**描述：** 从文件或输入流加载一个 `KvConfig` 实例。支持 JSON，YAML 和 XML 格式。

**参数：**

- `file (str | pathlib.Path)`：配置文件路径。

**用法：**

```python
cfg = Catenaconf.load("config.json")
```

**返回：**

- 返回一个由加载数据创建的 `KvConfig` 对象。

#### 从 Pydantic 模型创建

```python
Catenaconf.structured(model)
```

**描述：** 从一个 Pydantic 模型创建一个 `KvConfig` 实例。

**参数：**

- `model (pydantic.BaseModel)`：用于构建配置的 Pydantic 模型对象。

**用法：**

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field: str
cfg = Catenaconf.structured(MyModel(field="value"))
```

**返回：**

- 一个包含结构化配置的 `KvConfig` 对象。

### 更新配置

```python
Catenaconf.update(cfg, key, value=None, *, merge=True)
```

**描述：** 更新配置中指定键的值。

**参数：**

- `cfg (KvConfig)`：待更新的配置实例。
- `key (str)`：要更新值的位置，使用点号分隔的字符串。
- `value (Any, optional)`：新的值。
- `merge (bool, optional)`：是否合并字典。默认为 `True`。

**用法：**

```python
Catenaconf.update(cfg, "database.user", "root")
Catenaconf.update(cfg, "database", {"root": "root"})
Catenaconf.update(cfg, "database", {"root": "root"}, merge=True)
```

**注意：**

- 如果 `merge=True`，现有字典会与新值合并。
- 如果 `merge=False`，新值将取代现有值。

### 合并配置

```python
Catenaconf.merge(*configs)
```

**描述：** 将多个配置合并为一个。

**参数：**

- `*configs (KvConfig or dict)`：待合并的配置，作为位置参数传递。

**用法：**

```python
config1 = {"database": {"host": "localhost"}}
config2 = {"database": {"port": 3306}}

merged_cfg = Catenaconf.merge(config1, config2)
```

**返回：**

- 一个合并后的 `KvConfig` 实例。

### 引用与解析引用

```python
Catenaconf.resolve(cfg)
```

**描述：** 解析配置中的所有引用。引用以 `@{}` 格式定义。

**参数：**

- `cfg (KvConfig)`：包含引用的配置实例。

**用法：**

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

**注意：**

- 通过将占位符替换为实际值进行引用解析。

### 转换为字典

```python
Catenaconf.to_container(cfg, resolve=True)
```

**描述：** 将 `KvConfig` 实例转换为标准字典。

**参数：**

- `cfg (KvConfig)`：待转换的配置实例。
- `resolve (bool, optional)`：是否解析字典中的引用。默认为 `True`。

**用法：**

```python
dict_config = Catenaconf.to_container(cfg, resolve=True)
dict_config = Catenaconf.to_container(cfg, resolve=False)
```

**注意：**

- 当 `resolve=True` 时，配置中的所有引用将被解析。
- 当 `resolve=False` 时，引用将保持未解析状态。
