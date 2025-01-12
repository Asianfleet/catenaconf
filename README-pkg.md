<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD041 -->

<p align="center">
    <img src="https://tinypic.host/images/2025/01/06/-2025-01-06-03231131.png" alt="catenaconf logo" width=200 height=200 />
</p>
<h1 align="center">CatenaConf</h1>

<p align="center">
    <a href="https://pypi.org/project/pyecharts">
        <img src="https://img.shields.io/pypi/format/pyecharts.svg" alt="PyPI - Format">
    </a>
    <a href="https://github.com/pyecharts/pyecharts/pulls">
        <img src="https://img.shields.io/github/actions/workflow/status/Asianfleet/catenaconf/main.yaml" alt="build passing">
    </a>
    <a href="https://opensource.org/license/apache-2-0">
        <img src="https://img.shields.io/github/license/Asianfleet/catenaconf" alt="License">
    </a>
</p>

## Introduction

CatenaConf is a lightweight Python library designed for managing and operating configurations. It extends the Python dictionary type to manage configurations using key-value pairs and provides flexible operation functionalities.

## Features

- Lightweight: The code size is small and no third-party dependencies need to be installed (if you need to create a configuration from a Pydantic model or a yaml file, you need to install the corresponding dependencies).
- Dictionary based: Use Python dictionaries to create and manage configurations.
- Attribute access: Access and modify configuration values ​​through attributes, which is convenient and intuitive.
- Flexible update mechanism: Provides flexible update function and supports merging dictionaries.
- Reference resolution: Supports referencing other configuration values ​​in configuration values ​​and being able to resolve these references.

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

**Returns:**

- Returns a `KvConfig` object created from the dictionary.

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

**Description:** Load a KvConfig instance from a file. Supports JSON, YAML, and XML formats.

**Parameters:**

- `file (str | pathlib.Path)`: Path to the configuration file.

**Returns:**

- Returns a `KvConfig` object created from the loaded data.

**Usage:**

```python
cfg = Catenaconf.load("config.json")
```

#### Create from Pydantic Model

```python
Catenaconf.structured(model)
```

**Description:** Creates a `KvConfig` instance from a Pydantic model.

**Parameters:**

- `model (pydantic.BaseModel)`: A Pydantic model object to construct the configuration.

**Returns:**

- A `KvConfig` object containing the structured configuration.

**Usage:**

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field: str
cfg = Catenaconf.structured(MyModel(field="value"))
```

### Selecting Configuration Values

```python
Catenaconf.select(cfg, key, *, default="NOT FOUND", throw_on_resolution_failure=True, throw_on_missing=False)
```

**Description:** Selects a value from the configuration by key, with options for default values and error handling.

**Parameters:**

- `cfg (KvConfig)`: The configuration instance to select from.
- `key (str)`: The key to locate within the configuration.
- `default (Any, optional)`: The default value to return if the key is not found. Defaults to `"NOT FOUND"`.
- `throw_on_resolution_failure (bool, optional)`: Whether to raise an error if key resolution fails. Defaults to `True`.
- `throw_on_missing (bool, optional)`: Whether to raise an error for missing keys. Defaults to `False`.

**Returns:**

- The selected value, or the default value if the key is not found.

**Usage:**

```python
value = Catenaconf.select(cfg, "database.user", default=None, throw_on_resolution_failure=False)
```

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

**Returns:**

- A merged `KvConfig` instance.

**Usage:**

```python
config1 = {"database": {"host": "localhost"}}
config2 = {"database": {"port": 3306}}

merged_cfg = Catenaconf.merge(config1, config2)
```

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

**Returns:**

- A standard dictionary containing the configuration data.

**Usage:**

```python
dict_config = Catenaconf.to_container(cfg, resolve=True)
dict_config = Catenaconf.to_container(cfg, resolve=False)
```

**Notes:**

- When `resolve=True`, all references in the configuration are resolved.
- When `resolve=False`, references remain unresolved.
