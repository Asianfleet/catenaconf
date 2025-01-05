# Catenaconf

Catenaconf is a Python package for managing and operating configurations. It provides functionalities for creating, updating, merging, and parsing configurations.

## Installation

Install using pip:

```bash
pip install catenaconf
```

## Usage

### Create Configuration

Use the `Catenaconf.create` method to create a `DictConfig` instance:

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

### Update Configuration

Use the `Catenaconf.update` method to update the configuration:

```python
Catenaconf.update(cfg, "database.user", "root")
```

### Merge Configurations

Use the `Catenaconf.merge` method to merge multiple configurations:

```python
config1 = {"database": {"host": "localhost"}}
config2 = {"database": {"port": 3306}}

merged_cfg = Catenaconf.merge(config1, config2)
```

### Resolve Configuration

Use the `Catenaconf.resolve` method to resolve references in the configuration:

```python
config = {
    "path": "/data",
    "backup_path": "@{path}/backup"
}

cfg = Catenaconf.create(config)
Catenaconf.resolve(cfg)
```

### Convert to Dictionary

Use the `Catenaconf.to_container` method to convert a `DictConfig` instance to a regular dictionary:

```python
dict_config = Catenaconf.to_container(cfg)
```

## Catenaconf Class Features

- `create(config: dict) -> DictConfig`: Creates a `DictConfig` instance.
- `update(cfg: DictConfig, key: str, value: Any = None, *, merge: bool = True) -> None`: Updates the configuration, supporting nested updates.
- `merge(*configs) -> DictConfig`: Merges multiple configurations and returns a merged `DictConfig` instance.
- `resolve(cfg: DictConfig) -> None`: Resolves references in the configuration.
- `to_container(cfg: DictConfig) -> dict`: Converts a `DictConfig` instance to a regular dictionary.

## DictConfig Class Features

The `DictConfig` class extends Python's built-in `dict` class with the following features:

- Supports accessing dictionary items via attributes.
- Automatically converts nested dictionaries to `DictConfig` instances.
- Supports deep copying.
- Supports resolving references.
- Provides methods to convert `DictConfig` instances to regular dictionaries.
  