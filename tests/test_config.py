import unittest
from catenaconf import Catenaconf, KvConfig

class BaseCatenaconfTestCase(unittest.TestCase):
    def setUp(self):
        self.test_config = {
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
        self.dt = Catenaconf.create(self.test_config)


class TestDictConfig(BaseCatenaconfTestCase):
    """ test the KvConfig class """
    def test_get_underlined_key(self):
        test = {"__class__": "test"}
        dt = KvConfig(test)
        self.assertEqual(dt.__class__, KvConfig)
        
    def test_set_underlined_key(self):
        self.dt.__a__ = "a"
        self.dt.__b__ = "b"
        self.dt.b = {"c": "d"}
        self.dt.c = {"d": "e"}
        self.dt.e = [1, 2, 3]
        del self.dt.__b__
        self.dt.__to_container__()
        self.assertEqual(self.dt.__a__, "a")
        self.assertEqual(type(self.dt.__container__), dict)
  
  
class TestCatenaconfCreation(BaseCatenaconfTestCase):
    """ test the creation of Catenaconf """
    def test_create(self):
        self.assertIsInstance(self.dt, KvConfig)
        
    def test_create_with__list(self):
        dt = Catenaconf.create({"test": [1, 2, 3]})
        self.assertIsInstance(dt, KvConfig)
        

class TestCatenaconfResolution(BaseCatenaconfTestCase):
    """ test the resolution of Catenaconf """
    def test_resolve(self):
        Catenaconf.resolve(self.dt)
        self.assertEqual(self.dt["config"]["connection"], "Host: localhost, Port: 5432")
        self.assertEqual(self.dt["app"]["info"], "App Version: 1.0.0, Connection: Host: localhost, Port: 5432")

    def test_resolve_with_references(self):
        Catenaconf.update(self.dt, "config.database.host", "127.0.0.1")
        Catenaconf.resolve(self.dt)
        self.assertEqual(self.dt["config"]["connection"], "Host: 127.0.0.1, Port: 5432")


class TestCatenaconfUpdate(BaseCatenaconfTestCase):
    """ test the update of Catenaconf """
    def test_update(self):
        Catenaconf.update(self.dt, "config.database.host", "123")
        self.assertEqual(self.dt.config.database.host, "123")

    def test_update_non_existent_key(self):
        Catenaconf.update(self.dt, "config.database.username", "admin")
        self.assertEqual(self.dt.config.database.username, "admin")

    def test_update_with_merge(self):
        Catenaconf.update(self.dt, "config.database", {"host": "127.0.0.1", "port": 3306}, merge=True)
        self.assertEqual(self.dt.config.database.host, "127.0.0.1")
        self.assertEqual(self.dt.config.database.port, 3306)

    def test_update_without_merge(self):
        Catenaconf.update(self.dt, "config.database", {"host": "127.0.0.1", "port": 3306}, merge=False)
        self.assertEqual(self.dt.config.database.host, "127.0.0.1")
        self.assertEqual(self.dt.config.database.port, 3306)

    def test_update_with_non_dict_without_merge(self):
        Catenaconf.update(self.dt, "config.database", "new_value", merge=False)
        self.assertEqual(self.dt.config.database, "new_value")

    def test_update_with_new_key_with_merge(self):
        Catenaconf.update(self.dt, "test.test", "admin", merge=True)
        self.assertEqual(self.dt.test.test, "admin")


class TestCatenaconfMerge(BaseCatenaconfTestCase):
    """ test the merge of Catenaconf """
    def test_merge(self):
        ds = Catenaconf.merge(self.dt, {"new_key": "new_value"})
        self.assertIn("new_key", ds)
        self.assertEqual(ds["new_key"], "new_value")

    def test_merge_conflict(self):
        original = {"key": "original_value"}
        new = {"key": "new_value"}
        merged = Catenaconf.merge(original, new)
        self.assertEqual(merged["key"], "new_value")
        
    def test_merge_nested_dictionaries(self):
        original = {
            "config": {
                "database": {
                    "host": "localhost",
                    "port": 5432
                },
                "settings": {
                    "timeout": 30
                }
            }
        }
        new = {
            "config": {
                "database": {
                    "username": "admin"
                },
                "settings": {
                    "retry": 3
                }
            }
        }
        expected = {
            "config": {
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "username": "admin"
                },
                "settings": {
                    "timeout": 30,
                    "retry": 3
                }
            }
        }

        merged = Catenaconf.merge(KvConfig(original), KvConfig(new))
        self.assertEqual(Catenaconf.to_container(merged), expected)


class TestDictConfigMethods(BaseCatenaconfTestCase):
    def test_to_container(self):
        container = Catenaconf.to_container(self.dt)
        self.assertIsInstance(container, dict)
        self.assertEqual(container["config"]["database"]["host"], "localhost")

    def test_dictconfig_getattr(self):
        self.assertEqual(self.dt.config.database.host, "localhost")
        with self.assertRaises(AttributeError):
            _ = self.dt.config.database.invalid_key

    def test_dictconfig_setattr(self):
        self.dt.config.database.new_key = "new_value"
        self.assertEqual(self.dt.config.database.new_key, "new_value")

    def test_dictconfig_delattr(self):
        del self.dt.config.database.host
        with self.assertRaises(AttributeError):
            _ = self.dt.config.database.host

    def test_dictconfig_deepcopy(self):
        dt_copy = self.dt.deepcopy
        self.assertEqual(dt_copy.config.database.host, "localhost")
        dt_copy.config.database.host = "127.0.0.1"
        self.assertNotEqual(self.dt.config.database.host, dt_copy.config.database.host)

    def test_dictconfig_getallref(self):
        refs = self.dt.__ref__
        self.assertIn("config.database.host", refs)
        self.assertIn("config.database.port", refs)


""" if __name__ == '__main__':
    unittest.main() """
