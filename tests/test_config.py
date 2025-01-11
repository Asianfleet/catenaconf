import unittest
import json
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
import tempfile
import os
from catenaconf import Catenaconf, KvConfig
from catenaconf.ops import UnsupportedFormatError

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
            },
            "list":[
                {"a": 1, "b": 2},
                {"ref": "@{config.database.host}"}
            ]
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
        self.assertEqual(self.dt["list"][1]["ref"], "localhost")
    
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


class TestCatenaconfLoad(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Sample data for testing
        self.test_data = {
            "server": {
                "host": "localhost",
                "port": 8080
            },
            "database": {
                "url": "postgresql://localhost:5432",
                "username": "admin"
            }
        }
        
        # Create test files
        self._create_test_files()
    
    def tearDown(self):
        # Clean up temporary files
        for file in Path(self.test_dir).glob("*"):
            file.unlink()
        os.rmdir(self.test_dir)
    
    def _create_test_files(self):
        # Create JSON file
        json_path = Path(self.test_dir) / "config.json"
        with json_path.open("w") as f:
            json.dump(self.test_data, f)
            
        # Create YAML file
        yaml_path = Path(self.test_dir) / "config.yaml"
        with yaml_path.open("w") as f:
            yaml.dump(self.test_data, f)
            
        # Create XML file
        xml_path = Path(self.test_dir) / "config.xml"
        root = ET.Element("root")
        server = ET.SubElement(root, "server")
        ET.SubElement(server, "host").text = "localhost"
        ET.SubElement(server, "port").text = "8080"
        database = ET.SubElement(root, "database")
        ET.SubElement(database, "url").text = "postgresql://localhost:5432"
        ET.SubElement(database, "username").text = "admin"
        tree = ET.ElementTree(root)
        tree.write(xml_path)
        
        # Create empty files
        (Path(self.test_dir) / "empty.json").touch()
        (Path(self.test_dir) / "empty.yaml").touch()
        (Path(self.test_dir) / "empty.xml").touch()
        
    def test_load_json(self):
        """Test loading a valid JSON file"""
        config = Catenaconf.load(Path(self.test_dir) / "config.json")
        self.assertEqual(config["server"]["host"], "localhost")
        self.assertEqual(config["server"]["port"], 8080)
        self.assertEqual(config["database"]["url"], "postgresql://localhost:5432")
        self.assertEqual(config["database"]["username"], "admin")
        
    def test_load_yaml(self):
        """Test loading a valid YAML file"""
        config = Catenaconf.load(Path(self.test_dir) / "config.yaml")
        self.assertEqual(config["server"]["host"], "localhost")
        self.assertEqual(config["server"]["port"], 8080)
        self.assertEqual(config["database"]["url"], "postgresql://localhost:5432")
        self.assertEqual(config["database"]["username"], "admin")
        
    def test_load_xml(self):
        """Test loading a valid XML file"""
        config = Catenaconf.load(Path(self.test_dir) / "config.xml")
        self.assertEqual(config["server"]["host"], "localhost")
        self.assertEqual(config["server"]["port"], "8080")  # XML values are strings
        self.assertEqual(config["database"]["url"], "postgresql://localhost:5432")
        self.assertEqual(config["database"]["username"], "admin")
        
    def test_empty_files(self):
        """Test loading empty files of different formats"""
        empty_json = Catenaconf.load(Path(self.test_dir) / "empty.json")
        self.assertEqual(len(empty_json), 0)
        
        empty_yaml = Catenaconf.load(Path(self.test_dir) / "empty.yaml")
        self.assertEqual(len(empty_yaml), 0)
        
        empty_xml = Catenaconf.load(Path(self.test_dir) / "empty.xml")
        self.assertEqual(len(empty_xml), 0)
        
    def test_file_not_found(self):
        """Test loading a non-existent file"""
        with self.assertRaises(FileNotFoundError):
            Catenaconf.load(Path(self.test_dir) / "nonexistent.json")
            
    def test_unsupported_format(self):
        """Test loading a file with unsupported format"""
        # 创建一个 .txt 文件并写入一些内容
        unsupported_file = Path(self.test_dir) / "config.txt"
        unsupported_file.write_text('{"key": "value"}')  # 即使内容是有效的JSON格式，因为扩展名不支持，也应该抛出异常
        
        with self.assertRaises(UnsupportedFormatError) as context:
            Catenaconf.load(unsupported_file)
        
        # 验证异常信息
        self.assertEqual(str(context.exception), "Unsupported file format: .txt")

    def test_load_with_string_path(self):
        """Test loading using string path instead of Path object"""
        config = Catenaconf.load(str(Path(self.test_dir) / "config.json"))
        self.assertEqual(config["server"]["host"], "localhost")
        
    def test_complex_xml(self):
        """Test loading XML with nested elements and attributes"""
        xml_path = Path(self.test_dir) / "complex.xml"
        root = ET.Element("root")
        
        # Add nested elements
        services = ET.SubElement(root, "services")
        service1 = ET.SubElement(services, "service")
        ET.SubElement(service1, "name").text = "auth"
        ET.SubElement(service1, "port").text = "8081"
        
        service2 = ET.SubElement(services, "service")
        ET.SubElement(service2, "name").text = "api"
        ET.SubElement(service2, "port").text = "8082"
        
        tree = ET.ElementTree(root)
        tree.write(xml_path)
        
        config = Catenaconf.load(xml_path)
        self.assertEqual(len(config["services"]["service"]), 2)
        self.assertEqual(config["services"]["service"][0]["name"], "auth")
        self.assertEqual(config["services"]["service"][1]["port"], "8082")

""" if __name__ == '__main__':
    unittest.main() """
