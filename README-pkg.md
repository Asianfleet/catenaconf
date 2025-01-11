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

#### From `dict` object

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

- Use the `Catenaconf.create` method to create a configuration from a dictionary.
- The method returns a `KvConfig` instance.

#### `load` Function

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

#### `structured` Function

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
Catenaconf.update(cfg, "database.user", "root") # Adds a user key-value pair in database
Catenaconf.update(cfg, "database", {"root": "root"}) # Replaces the value of database with {"root": "root"}
Catenaconf.update(cfg, "database", {"root": "root"}, merge=True) # Adds a root key-value pair in database
```

- Use the `Catenaconf.update` method to update the configuration.
- The first parameter is the `KvConfig` instance to be updated, the second parameter specifies the location of the value to be updated, the third parameter is the new value, and the fourth parameter (merge) indicates whether to merge or not.
- merge parameter: Defaults to True. When set to True, if both the new value and the existing value are dictionaries, they will be merged instead of replacing the existing value. When set to False, the new value will directly replace the existing value.

### Merging Configurations

```python
config1 = {"database": {"host": "localhost"}}
config2 = {"database": {"port": 3306}}

merged_cfg = Catenaconf.merge(config1, config2)
```

- Use the `Catenaconf.merge` method to merge multiple configurations.
- Returns a merged `KvConfig` instance.

### References and Resolving References

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

- Use the `@{}` format to reference other configuration values.
- Use the `Catenaconf.resolve` method to resolve references within the configuration.

### Converting to Dictionary

```python
dict_config = Catenaconf.to_container(cfg, resolve=True)
dict_config = Catenaconf.to_container(cfg, resolve=False) # References within will not be resolved
```

- Use the `Catenaconf.to_container` method to convert a `KvConfig` instance into a regular dictionary.
- resolve parameter: Defaults to True. When set to True, internal references are resolved. When set to False, internal references are not resolved.
