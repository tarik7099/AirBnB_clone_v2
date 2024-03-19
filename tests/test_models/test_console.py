#!/usr/bin/python3
"""Defines unittests for console.py."""
import os
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.file_storage import FileStorage


class TestCreateCommand(unittest.TestCase):
    """Unittests for testing the create command in HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """Test setup."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Test teardown."""
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.HBNB

    def setUp(self):
        """Test setup."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Test teardown."""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_errors(self):
        """Test error handling in create command."""
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
        # Create instances and capture their IDs
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create BaseModel")
            bm_id = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create User")
            us_id = f.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            st_id = f.getvalue().strip()

        # Test if the created instances are in the output of "all" command
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all BaseModel")
            self.assertIn(bm_id, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            self.assertIn(us_id, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all State")
            self.assertIn(st_id, f.getvalue())

    def test_create_command_with_kwargs(self):
        """Test create command with additional kwargs."""
        # Test create command with additional key-value pairs
        with patch("sys.stdout", new=StringIO()) as f:
            call = "create Place city_id='0001' name='My_house' number_rooms=4 latitude=37.77 longitude=43.434"
            self.HBNB.onecmd(call)
            pl_id = f.getvalue().strip()

        # Test if the created instance and kwargs are in the output of "all" command
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            output = f.getvalue()
            self.assertIn(pl_id, output)
            self.assertIn("'city_id': '0001'", output)
            self.assertIn("'name': 'My_house'", output)
            self.assertIn("'number_rooms': 4", output)
            self.assertIn("'latitude': 37.77", output)
            self.assertIn("'longitude': 43.434", output)


if __name__ == "__main__":
    unittest.main()
