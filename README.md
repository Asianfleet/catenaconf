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

## Introduction

CatenaConf is a lightweight Python library designed for managing and operating configurations. It extends the Python dictionary type to manage configurations using key-value pairs and provides flexible operation functionalities.

## Features

- Lightweight: Depends only on the Python standard library, without any third-party dependencies.
- Based on Python dictionaries to create configurations.
- Access and modify configuration values via attributes.
- Flexible update and merge mechanisms.
- Ability to reference other configuration values within configuration values.

---

## Installation

Install using pip:

```bash
pip install catenaconf
```

## Usage

### Creating Configuration

#### Create from dictionary

```python
Catenaconf.create(config)
```

**Description:** Create a `KvConfig` instance (a built-in type of the library) from a dictionary.

**Parameters:**

- `config (dict)`: A dictionary containing the configuration data.

**Usage:**

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

#### Load from file

```python
Catenaconf.load(file)
```

**Description:** Load a KvConfig instance from a file or input stream. Supports JSON, YAML, and XML formats.

**Parameters:**

- `file (str | pathlib.Path)`: Path to the configuration file.

**Usage:**

```python
cfg = Catenaconf.load("config.json")
```

**Returns:**

- Returns a `KvConfig` object created from the loaded data.

#### Create from Pydantic Model

```python
Catenaconf.structured(model)
```

**Description:** Creates a `KvConfig` instance from a Pydantic model.

**Parameters:**

- `model (pydantic.BaseModel)`: A Pydantic model object to construct the configuration.

**Usage:**

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field: str
cfg = Catenaconf.structured(MyModel(field="value"))
```

**Returns:**

- A `KvConfig` object containing the structured configuration.

### Updating Configuration

```python
Catenaconf.update(cfg, key, value=None, *, merge=True)
```

**Description:** Updates the value of a specified key in the configuration.

**Parameters:**

- `cfg (KvConfig)`: The configuration instance to update.
- `key (str)`: The location of the value to be updated, specified as a dotted string.
- `value (Any, optional)`: The new value to set.
- `merge (bool, optional)`: Whether to merge dictionaries. Defaults to `True`.

**Usage:**

```python
Catenaconf.update(cfg, "database.user", "root")
Catenaconf.update(cfg, "database", {"root": "root"})
Catenaconf.update(cfg, "database", {"root": "root"}, merge=True)
```

**Notes:**

- If `merge=True`, existing dictionaries are merged with the new value.

- If `merge=False`, the new value replaces the existing one.

### Merging Configurations

```python
Catenaconf.merge(*configs)
```

**Description:** Merges multiple configurations into one.

**Parameters:**

- `*configs (KvConfig or dict)`: The configurations to merge, passed as positional arguments.

**Usage:**

```python
config1 = {"database": {"host": "localhost"}}
config2 = {"database": {"port": 3306}}

merged_cfg = Catenaconf.merge(config1, config2)
```

**Returns:**

- A merged `KvConfig` instance.

### References and Resolving References

```python
Catenaconf.resolve(cfg)
```

**Description:** Resolves all references in the configuration. References are defined with the `@{}` format.

**Parameters:**

- `cfg (KvConfig)`: The configuration instance containing the references.

**Usage:**

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

**Notes:**

- Resolves references by replacing placeholders with their actual values.

### Converting to Dictionary

```python
Catenaconf.to_container(cfg, resolve=True)
```

**Description:** Converts a `KvConfig` instance into a standard dictionary.

**Parameters:**

- `cfg (KvConfig)`: The configuration instance to convert.
- `resolve (bool, optional)`: Whether to resolve references in the dictionary. Defaults to `True`.

**Usage:**

```python
dict_config = Catenaconf.to_container(cfg, resolve=True)
dict_config = Catenaconf.to_container(cfg, resolve=False)
```

**Notes:**

- When `resolve=True`, all references in the configuration are resolved.
- When `resolve=False`, references remain unresolved.
