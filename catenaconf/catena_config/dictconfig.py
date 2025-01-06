import copy
import re

class DictConfig(dict):
    def __init__(self, *args, **kwargs):
        """ Initialize the DictConfig class, and the internal nested dictionary will also be converted to the DictConfig type """
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DictConfig(value)
            elif isinstance(value, list):
                self[key] = [DictConfig(item) if isinstance(item, dict) else item for item in value]

    # TODO: the DictConfig class may have special attributes with underlines, 
    # which can't accessd by super().__getattr__(key)
    def __getattr__(self, key):
        """ Get the value of the key """
        
        """
        The following two lines address such a situation:
        test = {"__class__": "test"}
        dt = DictConfig(test)
        At this time, dt.__class__ will return DictConfig instead of test.
        This is to ensure that special attributes cannot be used as key names.
        """
        if key.startswith('__') and key.endswith('__'):
            return super().__getattr__(key)

        try:
            value = self[key]
            # Return directly (the init function ensures that it is already of DictConfig type)
            return value
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        """ Set the value of the key """
        
        # make sure the special attributes are not overwritten by the key-value pair
        if key.startswith('__') and key.endswith('__'):
            super().__setattr__(key, value)
        else: 
            # Ensure that after adding new attributes, they will also be converted to DictConfig type
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
        """ Make a deep copy of an instance of the DictConfig class """
        # Use the default dict copying method to avoid infinite recursion.
        return DictConfig(copy.deepcopy(dict(self), memo))

    @property
    def deepcopy(self):
        """ Make a deep copy of an instance of the DictConfig class """
        return copy.deepcopy(self)  
    
    @property
    def __ref__(self):
        return self.__getallref__()
    
    def __getallref__(self):
        return re.findall(r'@\{(.*?)\}', self.__str__())
    
    @property
    def __container__(self) -> dict:
        """ Copy the DictConfig instance, convert it to a normal dict and output """
        return self.__to_container__()

    def __to_container__(self) -> dict:
        """ Copy the DictConfig instance, convert it to a normal dict and output """
        self_copy = self.deepcopy
        for key, value in self_copy.items():
            if isinstance(value, DictConfig):
                self_copy[key] = value.__to_container__()
            elif isinstance(value, dict):
                self_copy[key] = DictConfig(value).__to_container__()
        return dict(self_copy)