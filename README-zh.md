<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD041 -->

<p align="center">
    <img src="images/logo.png" alt="catenaconf logo" width=200 height=200 />
</p>
<h1 align="center">CatenaConf</h1>

<p align="center">
    <a href="https://github.com/pyecharts/pyecharts/actions">
        <img src="https://github.com/pyecharts/pyecharts/actions/workflows/python-app.yml/badge.svg" alt="Github Actions Status">
    </a>
    <a href="https://codecov.io/gh/pyecharts/pyecharts">
        <img src="https://codecov.io/gh/pyecharts/pyecharts/branch/master/graph/badge.svg" alt="Codecov">
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

# 简介

CatenaConf 是一个可用于管理和操作配置的极轻量 Python 库。它基于对 Python 字典类型的扩展，使用键值对管理配置，并提供灵活的操作功能。

# 特性

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
