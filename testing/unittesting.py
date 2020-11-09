import os
import app
import unittest
import tempfile
from flask import Flask

# code below referenced from Flask Documentation on Unit Testing:
# https://flask.palletsprojects.com/en/0.12.x/testing/

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.testing = True
        self.app = app.app.test_client()
        with app.app.app_context():
            app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])



    #Account creation
    def new_account(self, username, password, confirmpassword):
        return self.app.post('/signup', data=dict(
            username=username,
            password=password,
            confirmpassword=confirmpassword
        ), follow_redirects=True)

    def test_account_creation(self):
        #new account with no issues
        rv = self.new_account('testaccount','testpassword','testpassword')
        configure_routes
        assert b'Account Created!' in rv.data


    def test_username_already_taken(self):
        #username already taken
        rv = self.new_account('admin', 'testpassword', 'testpassword')
        assert b'Username is already taken.' in rv.data

    def test_password_dont_match(self):
        #passwords dont match
        rv = self.new_account('testaccount2', 'testpassword', 'estpassword')
        assert b'Passwords do not match!' in rv.data

    def test_password_too_short(self):
        #short password
        rv = self.new_account('testaccount3', 'word', 'word')
        assert b'Password must be more than 8 characters.' in rv.data



    #Log In (with a test accounts and the admin account)
    def login(self,username,password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    #since nothing flashes when logging in we have to find a different method for testing a successful login
    def test_login(self):
        rv = self.login('admin', 'admin')
        assert b'Username does not exist!' not in rv.data
        assert b'Incorrect password.' not in rv.data
        assert b'Create Resume' in rv.data

    def test_no_user_found(self):
        rv = self.login('testaccount4','password')
        assert b'Username does not exist!' in rv.data

    def test_incorrect_password(self):
        rv = self.login('admin','password')
        assert b'Incorrect password.' in rv.data



    #Creating Resume
    def createresume(self, name, age, work_exp, education_hs, education_college, graduated, skills, awards, contact):
        rv = self.app.post('/create_resume', data=dict(
            name=name,
            age=age,
            work_exp=work_exp,
            education_hs=education_hs,
            education_college=education_college,
            graduated=graduated,
            skills=skills,
            awards=awards,
            contact=contact
        ), follow_redirects=True)

    #need to find a way to actually check a database
    def test_resume_creation(self):
        self.login('admin', 'admin')
        self.createresume('Test Name', '19', '23 years', "HS C/o '19", "IWU C/o '23", '2023', 'All of them', 'Too Many', '302-555-1234, email@email.com')
        with app.app.app_context():
            db = app.get_db()
        assert b'Banana' in db
        #assert b'Test Name'





if __name__ == '__main__':
    unittest.main()