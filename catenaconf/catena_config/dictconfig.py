import copy
import re

class DictConfig(dict):
    def __init__(self, *args, **kwargs):
        """ 初始化 DictConfig 类，内部嵌套字典也会转换为 DictConfig 类型 """
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DictConfig(value)
            elif isinstance(value, list):
                self[key] = [DictConfig(item) if isinstance(item, dict) else item for item in value]

    def __getattr__(self, key):
        if key.startswith('__') and key.endswith('__'):
            return super().__getattr__(key)
        try:
            value = self[key]
            # 直接返回（init 函数保证其已经是 DictConfig 类型）
            return value
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        if key.startswith('__') and key.endswith('__'):
            super().__setattr__(key, value)
        else:   # 保证新加属性后，也会转换为 DictConfig 类型
            if isinstance(value, dict):
                value = DictConfig(value)
            elif isinstance(value, list):
                value = [DictConfig(item) if isinstance(item, dict) else item for item in value]
        
            self[key] = value

    def __delattr__(self, key):
        if key.startswith('__') and key.endswith('__'):
            super().__delattr__(key)
        else:
            del self[key]

    def __deepcopy__(self, memo):
        """ 对 DictConfig 类的实例进行深拷贝 """
        # Use the default dict copying method to avoid infinite recursion.
        return DictConfig(copy.deepcopy(dict(self), memo))

    @property
    def deepcopy(self):
        """ 对 DictConfig 类的实例进行深拷贝 """
        return copy.deepcopy(self)  
    
    @property
    def __ref__(self):
        return self.__getallref__()
    
    def __getallref__(self):
        return re.findall(r'@\{(.*)\}', self.__str__())
    
    @property
    def __container__(self) -> dict:
        """ 拷贝 DictConfig 实例，转换为普通的 dict 并输出 """
        return self.__to_container__()

    def __to_container__(self) -> dict:
        """ 拷贝 DictConfig 实例，转换为普通的 dict 并输出 """
        self_copy = self.deepcopy
        for key, value in self_copy.items():
            if isinstance(value, DictConfig):
                self_copy[key] = value.__to_container__()
            elif isinstance(value, dict):
                self_copy[key] = DictConfig(value).__to_container__()
        return dict(self_copy)