import copy
import re

class KvConfig(dict):
    def __init__(self, *args, **kwargs):
        """ Initialize the KvConfig class, and the internal nested dictionary will also be converted to the KvConfig type """
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = KvConfig(value)
            elif isinstance(value, list):
                self[key] = [KvConfig(item) if isinstance(item, dict) else item for item in value]

    # TODO: the KvConfig class may have special attributes with underlines, 
    # which can't accessd by super().__getattr__(key)
    def __getattr__(self, key):
        """ Get the value of the key """
        
        # The following two lines of code seems to be useless
        """ if key.startswith('__') and key.endswith('__'):
            return super().__getattr__(key) """

        try:
            value = self[key]
            # Return directly (the init function ensures that it is already of KvConfig type)
            return value
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        """ Set the value of the key """
        
        # make sure the special attributes are not overwritten by the key-value pair
        if key.startswith('__') and key.endswith('__'):
            super().__setattr__(key, value)
        else: 
            # Ensure that after adding new attributes, they will also be converted to KvConfig type
            if isinstance(value, dict):
                value = KvConfig(value)
            elif isinstance(value, list):
                value = [KvConfig(item) if isinstance(item, dict) else item for item in value]
        
            self[key] = value

    def __delattr__(self, key):
        if key.startswith('__') and key.endswith('__'):
            super().__delattr__(key)
        else:
            del self[key]

    def __deepcopy__(self, memo):
        """ Make a deep copy of an instance of the KvConfig class """
        # Use the default dict copying method to avoid infinite recursion.
        return KvConfig(copy.deepcopy(dict(self), memo))

    @property
    def deepcopy(self):
        """ Make a deep copy of an instance of the KvConfig class """
        return copy.deepcopy(self)  
    
    @property
    def __ref__(self):
        return self.__getallref__()
    
    def __getallref__(self):
        return re.findall(r'@\{(.*?)\}', self.__str__())
    
    @property
    def __container__(self) -> dict:
        """ Copy the KvConfig instance, convert it to a normal dict and output """
        return self.__to_container__()

    def __to_container__(self) -> dict:
        """ Copy the KvConfig instance, convert it to a normal dict and output """
        self_copy = self.deepcopy
        for key, value in self_copy.items():
            if isinstance(value, KvConfig):
                self_copy[key] = value.__to_container__()
            elif isinstance(value, dict):
                self_copy[key] = KvConfig(value).__to_container__()
        return dict(self_copy)