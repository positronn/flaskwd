# tests/test_user_model.py
import unittest
import time
from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)
    
    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password
    
    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))
    
    def test_password_salts_are_random(self):
        u = User(password = 'cat')
        u2 = User(password = 'cat')
        self.assertTrue(u.password_hash != u2.password_hash)
    
    def test_valid_confirmation_token(self):
        u = User(password = 'cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))
    
    def test_invalid_confirmation_token(self):
        u1 = User(password = 'cat')
        u2 = User(password = 'dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))
    
    def test_expired_confirmation_token(self):
        u = User(password = 'cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))
    
    def test_valid_reset_token(self):
        u = User(password = 'cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))
    
    def test_invalid_reset_token(self):
        u = User(password = 'cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + 'a', 'horse'))
        self.assertTrue(u.verify_password('cat'))
    
    def test_valid_email_change_token(self):
        u = User(email = 'mathew10@example.com', password = 'cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('rhianna10@example.org')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'rhianna10@example.org')

    def test_invalid_email_change_token(self):
        u1 = User(email = 'mathew11@example.com', password = 'cat')
        u2 = User(email = 'rhianna11@example.org', password = 'dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_email_change_token('david11@example.net')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'rhianna11@example.org')

    def test_duplicate_email_change_token(self):
        u1 = User(email='mathew6@example.com', password='cat')
        u2 = User(email='rhianna6@example.org', password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u2.generate_email_change_token('mathew6@example.com')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'rhianna6@example.org')