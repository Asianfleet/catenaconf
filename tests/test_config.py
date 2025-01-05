import unittest
from catenaconf import Catenaconf, DictConfig

class TestCatenaconf(unittest.TestCase):
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

    def test_create(self):
        self.assertIsInstance(self.dt, DictConfig)

    def test_resolve(self):
        Catenaconf.resolve(self.dt)
        self.assertEqual(self.dt["config"]["connection"], "Host: localhost, Port: 5432")
        self.assertEqual(self.dt["app"]["info"], "App Version: 1.0.0, Connection: Host: localhost, Port: 5432")

    def test_update(self):
        Catenaconf.update(self.dt, "config.database.host", "123")
        self.assertEqual(self.dt.config.database.host, "123")
    
    def test_update_non_existent_key(self):
        Catenaconf.update(self.dt, "config.database.username", "admin")
        self.assertEqual(self.dt.config.database.username, "admin")

    def test_merge(self):
        ds = Catenaconf.merge(self.dt, {"new_key": "new_value"})
        self.assertIn("new_key", ds)
        self.assertEqual(ds["new_key"], "new_value")

    def test_merge_conflict(self):
        original = {"key": "original_value"}
        new = {"key": "new_value"}
        merged = Catenaconf.merge(original, new)
        self.assertEqual(merged["key"], "new_value")

    def test_update_with_merge(self):
        Catenaconf.update(self.dt, "config.database", {"host": "127.0.0.1", "port": 3306}, merge=True)
        self.assertEqual(self.dt.config.database.host, "127.0.0.1")
        self.assertEqual(self.dt.config.database.port, 3306)

    def test_update_without_merge(self):
        Catenaconf.update(self.dt, "config.database", {"host": "127.0.0.1", "port": 3306}, merge=False)
        self.assertEqual(self.dt.config.database.host, "127.0.0.1")
        self.assertEqual(self.dt.config.database.port, 3306)

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

    def test_resolve_with_references(self):
        Catenaconf.update(self.dt, "config.database.host", "127.0.0.1")
        Catenaconf.resolve(self.dt)
        self.assertEqual(self.dt["config"]["connection"], "Host: 127.0.0.1, Port: 5432")

if __name__ == '__main__':
    unittest.main()
