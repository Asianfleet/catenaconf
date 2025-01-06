import re
from typing import Any
from .catena_config.kvconfig import KvConfig

class Catenaconf:
    @staticmethod
    def create(config: dict) -> KvConfig:
        """ Create a KvConfig instance """
        return KvConfig(config)

    @staticmethod
    def update(cfg: KvConfig, key: str, value: Any = None, *, merge: bool = True) -> None:
        keys = key.split('.')
        current = cfg
        for k in keys[:-1]:
            if k not in current:
                current[k] = KvConfig({})
            current = current[k]
        last_key = keys[-1]

        if merge:
            if isinstance(current.get(last_key, KvConfig({})), KvConfig):
                if isinstance(value, dict) or isinstance(value, KvConfig):
                    for k, v in value.items():
                        current[last_key][k] = v
                    current[last_key] = KvConfig(current[last_key])
                else:
                    current[last_key] = value
            else:
                    current[last_key] = value
        else:
            if isinstance(value, dict):
                current[last_key] = KvConfig(value)
            else:
                current[last_key] = value

    @staticmethod
    def merge(*configs) -> KvConfig:
        
        def merge_into(target: KvConfig, source: KvConfig) -> None:
            for key, value in source.items():
                if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                    merge_into(target[key], value)
                else:
                    target[key] = value
                    
        merged_config = KvConfig({})
        for config in configs:
            merge_into(merged_config, KvConfig(config))
        return KvConfig(merged_config)

    @staticmethod
    def resolve(cfg: KvConfig) -> None:
        capture_pattern = r'@\{(.*?)\}'
        def de_ref(captured):
            ref:str = captured.group(1)
            target = cfg
            for part in ref.split("."):
                target = target[part]
            return str(target)

        def sub_resolve(input: KvConfig):
            for key, value in input.items():
                if isinstance(value, KvConfig):
                    sub_resolve(value)
                elif isinstance(value, str):
                    if re.search(capture_pattern, value):
                        content = re.sub(capture_pattern, de_ref, value)
                        input[key] = content

        sub_resolve(cfg)

    @staticmethod
    def to_container(cfg: KvConfig, resolve = True) -> dict:
        """ convert KvConfig instance to a normal dict and output. """
        if resolve:
            cfg_copy = cfg.deepcopy
            Catenaconf.resolve(cfg_copy)
            return cfg_copy.__to_container__()
        else:
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