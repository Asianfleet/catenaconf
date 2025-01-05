import re
from typing import Any
from .catena_config.dictconfig import DictConfig

class Catenaconf:
    @staticmethod
    def create(config: dict) -> DictConfig:
        """ Create a DictConfig instance """
        return DictConfig(config)

    @staticmethod
    def update(cfg: DictConfig, key: str, value: Any = None, *, merge: bool = True) -> None:
        keys = key.split('.')
        current = cfg
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        last_key = keys[-1]

        if merge:
            if isinstance(current.get(last_key, DictConfig({})), DictConfig):
                if isinstance(value, dict) or isinstance(value, DictConfig):
                    for k, v in value.items():
                        current[last_key][k] = v
                    current[last_key] = DictConfig(current[last_key])
                else:
                    current[last_key] = value
            else:
                    current[last_key] = value
        else:
            if isinstance(value, dict):
                current[last_key] = DictConfig(value)
            else:
                current[last_key] = value

    @staticmethod
    def merge(*configs) -> DictConfig:
        
        def merge_into(target: DictConfig, source: DictConfig) -> None:
            for key, value in source.items():
                if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                    merge_into(target[key], value)
                else:
                    target[key] = value
                    
        merged_config = DictConfig({})
        for config in configs:
            merge_into(merged_config, DictConfig(config))
        return DictConfig(merged_config)

    @staticmethod
    def resolve(cfg: DictConfig) -> None:
        capture_pattern = r'@\{(.*?)\}'
        def de_ref(captured):
            ref:str = captured.group(1)
            target = cfg
            for part in ref.split("."):
                target = target[part]
            return str(target)

        def sub_resolve(input: DictConfig):
            for key, value in input.items():
                if isinstance(value, DictConfig):
                    sub_resolve(value)
                elif isinstance(value, str):
                    if re.search(capture_pattern, value):
                        content = re.sub(capture_pattern, de_ref, value)
                        input[key] = content

        sub_resolve(cfg)

    @staticmethod
    def to_container(cfg: DictConfig) -> dict:
        return cfg.__to_container__()
    


""" if __name__ == "__main__":
    
    test = {
        "config": {
            "database": {
                "host": "localhost",
                "port": 5432
            },
            "connection": "Host: @{config.database.host}, Port: @{config.database.port}"
        },
        "app": {
            "version": "1.0.0",
            "info": "App Version: @{app.version}, Connection: @{config.connection}"
        }
    }
    
    print(test)

    dt = Catenaconf.create(test)
    Catenaconf.resolve(dt)
    print(dt)

    dt.config.database.host = "123"
    print(dt)

    Catenaconf.update(dt, "config.database", {"123": "123"})
    print(dt)

    ds = Catenaconf.merge(dt, {"new_key": "new_value"})
    print(ds)
    
    Catenaconf.update(dt, "config.database.host", "4567")
    print(dt) """