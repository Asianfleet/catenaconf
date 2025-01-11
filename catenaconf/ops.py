import re
import json
from pathlib import Path
from pydantic import BaseModel
from typing import Any, IO, Union
import xml.etree.ElementTree as ET

from .catena_config.kvconfig import KvConfig

try:
    from pydantic import BaseModel
except ImportError:
    raise ImportError("Pydantic is not installed. Please install it with `pip install pydantic`.")

class UnsupportedFormatError(Exception):
    """Raised when the file format is unsupported or the content cannot be parsed."""

class Catenaconf:
    @staticmethod
    def create(config: dict) -> KvConfig:
        """ Create a KvConfig instance """
        return KvConfig(config)

    @staticmethod
    def structured(model: BaseModel) -> KvConfig:
        """ Creates a KvConfig instance from a Pydantic model """
        return KvConfig(model.model_dump())

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

    # TODO: Consider the case of referencing an element in a list
    @staticmethod
    def resolve(cfg: KvConfig) -> None:
        capture_pattern = r'@\{(.*?)\}'
        def de_ref(captured):
            ref: str = captured.group(1)
            target = cfg
            for part in ref.split("."):
                target = target[part]
            return str(target)
        def sub_resolve(input_: KvConfig | list):
            for key, value in input_.items():
                if isinstance(value, KvConfig):
                    sub_resolve(value)
                elif isinstance(value, str):
                    if re.search(capture_pattern, value):
                        content = re.sub(capture_pattern, de_ref, value)
                        input_[key] = content
                elif isinstance(value, list):
                    for item in value:
                        sub_resolve(item)
                        
        sub_resolve(cfg)

    @staticmethod
    def to_container(cfg: KvConfig, resolve=True) -> dict:
        """ convert KvConfig instance to a normal dict and output. """
        if resolve:
            cfg_copy = cfg.deepcopy
            Catenaconf.resolve(cfg_copy)
            return cfg_copy.__to_container__()
        else:
            return cfg.__to_container__()

    @staticmethod
    def load(file: Union[str, Path]) -> KvConfig:
        """
        Load a KvConfig instance from a file or input stream.
        
        Supports JSON, YAML, XML, and CSV formats. 
        """
        
        try:
            import yaml
        except ImportError:
            raise ImportError("YAML is not installed. Please install it with `pip install pyyaml`.")
        
        path = Path(file)
        if not path.exists():
            raise FileNotFoundError(f"File {path} does not exist.")
        
        # 首先检查文件扩展名
        suffix = path.suffix.lower()
        if suffix not in ['.json', '.yaml', '.yml', '.xml']:
            raise UnsupportedFormatError(f"Unsupported file format: {suffix}")
        
        # 读取文件内容
        content = path.read_text(encoding='utf-8').strip()
        
        # 处理空文件
        if not content:
            return KvConfig({})
        
        # 根据文件类型解析内容
        try:
            if suffix == '.json':
                config = json.loads(content)
            elif suffix in ['.yaml', '.yml']:
                config = yaml.safe_load(content)
            else:  # .xml
                root = ET.fromstring(content)
                config = Catenaconf._xml_to_dict(root)
                
            return KvConfig(config)
        except (json.JSONDecodeError, yaml.YAMLError, ET.ParseError) as e:
            raise UnsupportedFormatError(f"Failed to parse {suffix} file: {str(e)}")

    @staticmethod
    def _xml_to_dict(element: ET.Element) -> dict:
        """Convert an XML element and its children to a dictionary."""
        result = {}
        for child in element:
            child_result = Catenaconf._xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_result)
            else:
                result[child.tag] = child_result
        if element.text and element.text.strip():
            if result:
                result['text'] = element.text.strip()
            else:
                return element.text.strip()
        return result
        
        
