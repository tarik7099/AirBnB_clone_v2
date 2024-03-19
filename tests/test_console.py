import unittest
from console import HBNBCommand
from models import storage
from unittest.mock import patch
from io import StringIO


class TestCreateCommand(unittest.TestCase):
    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        storage.delete_all()

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_instance(self, mock_stdout):
        self.console.onecmd('create BaseModel name="test" age=25')
        output = mock_stdout.getvalue().strip()
        self.assertTrue(len(output) == 36)  # Verify object ID length
        self.assertIn('BaseModel', storage.all().keys())  # Verify object is stored
        obj = storage.all()['BaseModel']
        self.assertEqual(obj.name, 'test')  # Verify parameter value
        self.assertEqual(obj.age, 25)  # Verify parameter value

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_invalid_syntax(self, mock_stdout):
        self.console.onecmd('create BaseModel name="test" age=abc')
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** invalid value for parameter 'age' **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_missing_class(self, mock_stdout):
        self.console.onecmd('create MyModel name="test"')
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_missing_class_name(self, mock_stdout):
        self.console.onecmd('create')
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_invalid_param_syntax(self, mock_stdout):
        self.console.onecmd('create BaseModel name=test')
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "** invalid syntax for parameter: 'name=test' **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_multiple_instances(self, mock_stdout):
        # Create multiple instances of BaseModel with different parameters
        self.console.onecmd('create BaseModel name="obj1" age=10')
        self.console.onecmd('create BaseModel name="obj2" age=20')
        self.console.onecmd('create BaseModel name="obj3" age=30')
        self.assertEqual(len(storage.all()), 3)  # Verify three instances are created

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_float_param(self, mock_stdout):
        self.console.onecmd('create BaseModel value=3.14')
        obj = storage.all()['BaseModel']
        self.assertEqual(obj.value, 3.14)  # Verify float parameter value

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_string_param(self, mock_stdout):
        self.console.onecmd('create BaseModel text="hello world"')
        obj = storage.all()['BaseModel']
        self.assertEqual(obj.text, 'hello world')  # Verify string parameter value


if __name__ == "__main__":
    unittest.main()
