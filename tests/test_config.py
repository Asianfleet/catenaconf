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

    def test_merge(self):
        ds = Catenaconf.merge(self.dt, {"new_key": "new_value"})
        self.assertIn("new_key", ds)
        self.assertEqual(ds["new_key"], "new_value")

if __name__ == '__main__':
    unittest.main()
