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

CatenaConf 是一个可用于管理和操作配置的极轻量 Python 库。它基于对 Python 字典类型的扩展，使用键值对管理配置，并提供灵活的操作功能。

## 特性

- 轻量级：仅依赖 Python 标准库，不依赖其他第三方库。
- 基于 Python 字典创建配置
- 通过属性访问与修改配置值
- 灵活的更新与合并机制
- 可在配置值中引用其他配置值

## 安装

使用 pip 安装：

```bash
pip install catenaconf
```

## 使用方法

### 创建配置

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

- 使用 `Catenaconf.create` 方法从字典创建配置
- 方法返回一个 `KvConfig` 实例

### 更新配置

```python
Catenaconf.update(cfg, "database.user", "root") # 将在 database 中添加 user 键值对
Catenaconf.update(cfg, "database", {"root": "root"}) # 将 database 的值替换为 {"root": "root"}
Catenaconf.update(cfg, "database", {"root": "root"}, merge = True) # 在 database 中添加 root 键值对
```

- 使用 `Catenaconf.update` 方法更新配置
- 第一个参数为待更新的 `KvConfig` 实例， 第二个参数用于指定要更新的值对应的位置，第三个参数为新值，第四个参数（merge）为是否合并
- merge 参数：默认为 True， 当为 True 时，如果新值与原有值均为键值对，则会将新值与原有值进行合并而不是直接替换原有值。当为 False 时，新值将直接替换原有值。

### 合并配置

```python
config1 = {"database": {"host": "localhost"}}
config2 = {"database": {"port": 3306}}

merged_cfg = Catenaconf.merge(config1, config2)
```

- 使用 `Catenaconf.merge` 方法合并多个配置
- 返回一个合并后的 `KvConfig` 实例

### 引用与解析引用

```python
config = {
    "info":{
        "path": "/data",
        "filename": "a.txt"
    },
    "backup_path": "@{info.path}/backup/@{info.filename}"
}

cfg = Catenaconf.create(config)
Catenaconf.resolve(cfg)
```

- 使用 `@{}` 格式引用其他配置值
- 使用 `Catenaconf.resolve` 方法解析配置中的引用：

### 转换为字典

```python
dict_config = Catenaconf.to_container(cfg, resolve = True)
dict_config = Catenaconf.to_container(cfg, resolve = False) # 此时内部的引用不会被解析
```

- 使用 `Catenaconf.to_container` 方法将 `KvConfig` 实例转换为普通字典
- resolve 参数：默认为 True， 当为 True 时，内部的引用会被解析，当为 False 时，内部的引用不会被解析
