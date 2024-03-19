#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import console
import inspect
import pep8
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.file_storage import FileStorage

HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")


class TestHBNBCommand(unittest.TestCase):
    """Unittests for testing the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """HBNBCommand testing setup.

        Temporarily rename any existing file.json.
        Reset FileStorage objects dictionary.
        Create an instance of the command interpreter.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        # Create an instance of the HBNBCommand class. This allows the test
        # methods within the class to access and use this instance during the
        # testing process.
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """HBNBCommand testing teardown.

        Restore original file.json.
        Delete the test HBNBCommand instance.
        """
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.HBNB

    def setUp(self):
        """Reset FileStorage objects dictionary."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Delete any created file.json."""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_create_for_errors(self):
        """Test create command errors."""
        # Test if class name is missing
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        # Test if class doesn't exist
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    def test_create_command_validity(self):
        """Test create command."""
        # Create BaseModel instance and capture its ID
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            bm = f.getvalue().strip()

        # Create User instance and capture its ID
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create User")
            us = f.getvalue().strip()

        # Create State instance and capture its ID
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            st = f.getvalue().strip()

        # Create Place instance and capture its ID
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Place")
            pl = f.getvalue().strip()

        # Create City instance and capture its ID
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create City")
            ct = f.getvalue().strip()

        # Create Review instance and capture its ID
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Review")
            rv = f.getvalue().strip()

        # Create Amenity instance and capture its ID
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Amenity")
            am = f.getvalue().strip()
        # Test if the created instances are in the output of "all" command
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all BaseModel")
            self.assertIn(bm, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            self.assertIn(us, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all State")
            self.assertIn(st, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            self.assertIn(pl, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all City")
            self.assertIn(ct, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Review")
            self.assertIn(rv, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Amenity")
            self.assertIn(am, f.getvalue())

    def test_create_command_with_kwargs(self):
        """Test create command with kwargs."""
        # Test create command with additional key-value pairs
        with patch("sys.stdout", new=StringIO()) as f:
            call = ('create Place city_id="0001" name="My_house" number_rooms=4 latitude=37.77 longitude=43.434')
            self.HBNB.onecmd(call)
            pl = f.getvalue().strip()
         # Test if the created instance and kwargs are in the
         #    output of "all" command
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            output = f.getvalue()
            self.assertIn(pl, output)
            self.assertIn("'city_id': '0001'", output)
            self.assertIn("'name': 'My_house'", output)
            self.assertIn("'number_rooms': 4", output)
            self.assertIn("'latitude': 37.77", output)
            self.assertIn("'longitude': 43.434", output)

    def test_create_command_with_invalid_kwargs(self):
        """Test create command with invalid kwargs."""
        # Test create command with invalid key-value pairs
        with patch("sys.stdout", new=StringIO()) as f:
            call = ('create Place invalid_key="invalid_value"')
            self.HBNB.onecmd(call)
            output = f.getvalue().strip()
            self.assertEqual(output, "** Unknown attribute **")

    def test_create_command_invalid_class(self):
        """Test create command with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create InvalidClassName")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

    def test_create_command_missing_class(self):
        """Test create command with missing class name."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

    def test_emptyline(self):
        """Test emptyline method of HBNBCommand."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("\n")
            output = f.getvalue().strip()
            self.assertEqual(output, "")

    def test_quit(self):
        """Test quit command."""
        with self.assertRaises(SystemExit):
            self.HBNB.onecmd("quit")

    def test_EOF(self):
        """Test EOF command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(self.HBNB.onecmd("EOF"))
            output = f.getvalue().strip()
            self.assertTrue(output == "")

    def test_help(self):
        """Test help command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("help")
            output = f.getvalue().strip()
            self.assertTrue("EOF  all  create  destroy  help  quit  show  update" in output)

    def test_help_quit(self):
        """Test help quit command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("help quit")
            output = f.getvalue().strip()
            self.assertTrue("Quit command to exit the program" in output)

    def test_help_EOF(self):
        """Test help EOF command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("help EOF")
            output = f.getvalue().strip()
            self.assertTrue("EOF command (Ctrl-D)" in output)

    def test_help_create(self):
        """Test help create command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("help create")
            output = f.getvalue().strip()
            self.assertTrue("Creates a new instance of BaseModel" in output)

    def test_help_all(self):
        """Test help all command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("help all")
            output = f.getvalue().strip()
            self.assertTrue("Prints all string representation" in output)

    def test_help_show(self):
        """Test help show command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("help show")
            output = f.getvalue().strip()
            self.assertTrue("Prints the string representation" in output)

    def test_help_destroy(self):
        """Test help destroy command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("help destroy")
            output = f.getvalue().strip()
            self.assertTrue("Deletes an instance" in output)

    def test_help_update(self):
        """Test help update command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("help update")
            output = f.getvalue().strip()
            self.assertTrue("Updates an instance" in output)

    def test_create_with_int_value(self):
        """Test create command with integer value."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel my_number=8")
            output = f.getvalue().strip()
            self.assertTrue(len(output) == 36)

    def test_create_with_float_value(self):
        """Test create command with float value."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel my_float=3.14")
            output = f.getvalue().strip()
            self.assertTrue(len(output) == 36)

    def test_create_with_list_value(self):
        """Test create command with list value."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create BaseModel my_list="[1, 2, 3]"')
            output = f.getvalue().strip()
            self.assertTrue(len(output) == 36)

    def test_create_with_dict_value(self):
        """Test create command with dictionary value."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create BaseModel my_dict="{\'key\': \'value\'}"')
            output = f.getvalue().strip()
            self.assertTrue(len(output) == 36)

    def test_create_with_invalid_dict(self):
        """Test create command with invalid dictionary."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create BaseModel my_dict="[{\'key\': 5}"')
            output = f.getvalue().strip()
            self.assertEqual(output, "** Invalid format **")

    def test_show_valid(self):
        """Test show command with valid arguments."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel my_number=8")
            bm_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd(f"show BaseModel {bm_id}")
            output = f.getvalue().strip()
            self.assertTrue(bm_id in output)
            self.assertTrue("BaseModel" in output)

    def test_show_invalid(self):
        """Test show command with invalid arguments."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show BaseModel")
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show BaseModel 12345")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_destroy_valid(self):
        """Test destroy command with valid arguments."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            bm_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd(f"destroy BaseModel {bm_id}")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd(f"show BaseModel {bm_id}")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_destroy_invalid(self):
        """Test destroy command with invalid arguments."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy BaseModel")
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy BaseModel 12345")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_update_valid(self):
        """Test update command with valid arguments."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            bm_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd(f"update BaseModel {bm_id} name 'test'")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd(f"show BaseModel {bm_id}")
            output = f.getvalue().strip()
            self.assertTrue("'name': 'test'" in output)

    def test_update_invalid(self):
        """Test update command with invalid arguments."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update BaseModel")
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update BaseModel 12345")
            output = f.getvalue().strip()
            self.assertEqual(output, "** attribute name missing **")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('update BaseModel 12345 name "test"')
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            bm_id = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd(f"update BaseModel {bm_id} my_name 'test'")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

if __name__ == "__main__":
    unittest.main()
