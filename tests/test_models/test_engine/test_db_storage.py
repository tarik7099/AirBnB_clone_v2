#!/usr/bin/python3
"""Defines unnittests for models/engine/db_storage.py."""
import pep8
import models
import MySQLdb
import unittest
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine


class TestDBStorage(unittest.TestCase):
    """Unittests for testing the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """DBStorage testing setup.

        Instantiate new DBStorage.
        Fill DBStorage test session with instances of all classes.
        """
        if type(models.storage) == DBStorage:
            cls.storage = DBStorage()
            Base.metadata.create_all(cls.storage._DBStorage__engine)
            Session = sessionmaker(bind=cls.storage._DBStorage__engine)
            cls.storage._DBStorage__session = Session()
            cls.state_obj = State(name="California")
            cls.storage._DBStorage__session.add(cls.state_obj)
            cls.city_obj = City(name="San_Jose", state_id=cls.state_obj.id)
            cls.storage._DBStorage__session.add(cls.city_obj)
            cls.user_obj = User(email="poppy@holberton.com", password="betty")
            cls.storage._DBStorage__session.add(cls.user_obj)
            cls.place_obj = Place(city_id=cls.city_obj.id, user_id=cls.user_obj.id,
                              name="School")
            cls.storage._DBStorage__session.add(cls.place_obj)
            cls.amenity_obj = Amenity(name="Wifi")
            cls.storage._DBStorage__session.add(cls.amenity_obj)
            cls.review_obj = Review(place_id=cls.place_obj.id, user_id=cls.user_obj.id,
                                text="stellar")
            cls.storage._DBStorage__session.add(cls.review_obj)
            cls.storage._DBStorage__session.commit()

    @classmethod
    def tearDownClass(cls):
        """DBStorage testing teardown.

        Delete all instantiated test classes.
        Clear DBStorage session.
        """
        if type(models.storage) == DBStorage:
            cls.storage._DBStorage__session.delete(cls.state_obj)
            cls.storage._DBStorage__session.delete(cls.city_obj)
            cls.storage._DBStorage__session.delete(cls.user_obj)
            cls.storage._DBStorage__session.delete(cls.amenity_obj)
            cls.storage._DBStorage__session.commit()
            del cls.state_obj
            del cls.city_obj
            del cls.user_obj
            del cls.place_obj
            del cls.amenity_obj
            del cls.review_obj
            cls.storage._DBStorage__session.close()
            del cls.storage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_attributes(self):
        """Check for attributes."""
        self.assertTrue(isinstance(self.storage._DBStorage__engine, Engine))
        self.assertTrue(isinstance(self.storage._DBStorage__session, Session))

    def test_methods(self):
        """Check for methods."""
        self.assertTrue(hasattr(DBStorage, "__init__"))
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.storage, DBStorage))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_all(self):
        """Test default all method."""
        obj = self.storage.all()
        self.assertEqual(type(obj), dict)
        self.assertEqual(len(obj), 6)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_all_cls(self):
        """Test all method with specified cls."""
        obj = self.storage.all(State)
        self.assertEqual(type(obj), dict)
        self.assertEqual(len(obj), 1)
        self.assertEqual(self.state_obj, list(obj.values())[0])

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_new(self):
        """Test new method."""
        state = State(name="Washington")
        self.storage.new(state)
        store = list(self.storage._DBStorage__session.new)
        self.assertIn(state, store)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save(self):
        """Test save method."""
        state = State(name="Virginia")
        self.storage._DBStorage__session.add(state)
        self.storage.save()
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM states WHERE BINARY name = 'Virginia'")
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(state.id, query[0][0])
        cursor.close()

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_delete(self):
        """Test delete method."""
        state = State(name="New_York")
        self.storage._DBStorage__session.add(state)
        self.storage._DBStorage__session.commit()
        self.storage.delete(state)
        self.assertNotIn(state, list(self.storage._DBStorage__session.query(State)))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_delete_none(self):
        """Test delete method with None."""
        try:
            self.storage.delete(None)
        except Exception:
            self.fail

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_reload(self):
        """Test reload method."""
        og_session = self.storage._DBStorage__session
        self.storage.reload()
        self.assertIsInstance(self.storage._DBStorage__session, Session)
        self.assertNotEqual(og_session, self.storage._DBStorage__session)
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session = og_session


if __name__ == "__main__":
    unittest.main()
