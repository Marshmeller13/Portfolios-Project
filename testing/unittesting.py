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

#URLs to be checked
    #/ (root)            X
    #/show_template      X
    #/create_template    X
    #/login              X
    #/upload             X
    #/insert_resume      'position' form needs resolved
    #/signup             X
    #/delete_resume      X
    #/profile_page       X
    #  -red              X
    #  -green            X
    #  -teal             X
    #/resumes            X
    #/edit_resume        X
    #/edit_page          Can't test
    #/get_blob           Can't test
    #/docs/<id>          Can't test - can't simulate session id
    #/<id>               Can't test - can't simulate session id
    #/uploaded_list      'position' form needs resolved
    #/delete_uploaded    Can't test - 'position' form needs resolved
    #/profile_form       Can't test - can't simulate session id
    #/edit_profile       Can't test - can't simulate session id
    #/edit_profile_form  Can't test - can't simulate session id
    #/create_porfile     Can't test - can't simulate session id
    #/docs/pic<id>       Can't test - can't simulate session id



    #
    #root testing (/) (checks data from /login to make sure its on the right page)
    #
    def test_root(self):
        rv = self.app.get('/')
        assert b'You should be redirected automatically to target URL:' in rv.data


    #
    #show template (/show_template) (checking to make sure resume_template_orig.html loads correctly)
    #
    def test_show_template(self):
        rv = self.app.get('/show_template')
        assert b'Create Resume' in rv.data


    #
    # Creating Resume (/create_resume)
    #
    def create_resume(self, name, age, work_exp, education_hs, education_college, graduated, skills, awards,
                     contact):
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

    def test_resume_creation(self):
        self.login('admin', 'admin')
        self.create_resume('Test Name', '19', '23 years', "HS C/o '19", "IWU C/o '23", '2023', 'All of them', 'Too Many', '302-555-1234, email@email.com')
        with app.app.app_context():
            db = app.get_db()
            rv = db.execute('SELECT * from resume_entries WHERE id = ?', ('1',)).fetchone()
        assert 'Test Name' in rv
        assert '19' in rv
        assert '23 years' in rv
        assert "HS C/o '19" in rv
        assert "IWU C/o '23" in rv
        assert '2023' in rv
        assert 'All of them' in rv
        assert 'Too Many' in rv
        assert '302-555-1234, email@email.com' in rv


    #
    #Log In (with a test accounts and the admin account)
    #
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


    #
    # Upload (/upload) (check to make sure upload.html loaded correctly)
    #
    def test_upload(self):
        rv = self.app.get('/upload')
        assert b'input type = "file"' in rv.data

    #
    # Insert Resume (/insert_resume) (will check to make sure an entry is found in the uploaded resume table)
    # ---Need to resolve 'position' form---
    def insert_resume(self):
        testfile = open('testpicture.png')
        return self.app.post('/insert_resume', data=dict(
            file=testfile,
            position='None'
        ), follow_redirects=True)


    #
    # Account creation (/signup)
    #
    def new_account(self, username, password, confirmpassword):
        return self.app.post('/signup', data=dict(
            username=username,
            password=password,
            confirmpassword=confirmpassword
        ), follow_redirects=True)

    def test_account_creation(self):
        # new account with no issues
        rv = self.new_account('testaccount', 'testpassword', 'testpassword')
        assert b'Account Created!' in rv.data
        with app.app.app_context():
            db = app.get_db()
            rv = db.execute('SELECT * FROM user WHERE username = ?', ('testaccount',)).fetchone()
        assert 'testaccount' in rv

    def test_username_already_taken(self):
        # username already taken
        rv = self.new_account('admin', 'testpassword', 'testpassword')
        assert b'Username is already taken.' in rv.data

    def test_password_dont_match(self):
        # passwords dont match
        rv = self.new_account('testaccount2', 'testpassword', 'estpassword')
        assert b'Passwords do not match!' in rv.data

    def test_password_too_short(self):
        # short password
        rv = self.new_account('testaccount3', 'word', 'word')
        assert b'Password must be more than 8 characters.' in rv.data


    #
    #Deleting resume (/delete)
    #
    def deleteresume(self, id):
        return self.app.post('/delete_resume', data=dict(
            delete=id
        ), follow_redirects=True)

    def test_delete_resume(self):
        self.login('admin','admin')
        self.create_resume('Test Name', '19', '23 years', "HS C/o '19", "IWU C/o '23", '2023', 'All of them',
                           'Too Many', '302-555-1234, email@email.com')
        with app.app.app_context():
            db = app.get_db()
            rv = db.execute('SELECT * FROM resume_entries WHERE id=1').fetchone()
        assert 'Test Name' in rv
        assert '19' in rv
        assert '23 years' in rv
        assert "HS C/o '19" in rv
        assert "IWU C/o '23" in rv
        assert '2023' in rv
        assert 'All of them' in rv
        assert 'Too Many' in rv
        assert '302-555-1234, email@email.com' in rv

        self.deleteresume('1')

        with app.app.app_context():
            db = app.get_db()
            rv = db.execute('SELECT * FROM resume_entries').fetchall()
        assert 'Test Name' not in rv
        assert '19' not in rv
        assert '23 years' not in rv
        assert "HS C/o '19" not in rv
        assert "IWU C/o '23" not in rv
        assert '2023' not in rv
        assert 'All of them' not in rv
        assert 'Too Many' not in rv
        assert '302-555-1234, email@email.com' not in rv


    #
    # Profile Page (/profile_page) (check for correct redirect)
    #
    def test_profile_page(self):
        rv = self.app.get('/profile_page')
        assert b'<!--Profile Display-->' in rv.data

    ## red profile page
    def test_profile_page_red(self):
        rv = self.app.get('/profile_page_red')
        assert b'static/styles_profile_red.css' in rv.data

    ## green profile page
    def test_profile_page_green(self):
        rv = self.app.get('/profile_page_green')
        assert b'static/styles_profile_green.css' in rv.data

    ## teal profile page
    def test_profile_page_teal(self):
        rv = self.app.get('/profile_page_teal')
        assert b'static/styles_profile_teal.css' in rv.data


    #
    # Resume Display (/resumes)
    #
    def test_resumes(self):
        self.login('admin', 'admin')
        self.create_resume('Test Name', '19', '23 years', "HS C/o '19", "IWU C/o '23", '2023', 'All of them',
                           'Too Many', '302-555-1234, email@email.com')
        rv = self.app.get('/resumes')
        assert b'Test Name' in rv.data
        assert b'19' in rv.data
        assert b'23 years' in rv.data
        #changed apostrophe to unicode
        assert b'HS C/o &#39;19' in rv.data
        assert b'IWU C/o &#39;23' in rv.data
        assert b'2023' in rv.data
        assert b'All of them' in rv.data
        assert b'Too Many' in rv.data
        assert b'302-555-1234, email@email.com' in rv.data


    #
    # Editing Resumes (/edit_resumes)
    #
    def test_edit_resume(self):
        self.login('admin', 'admin')
        self.create_resume('Test Name', '19', '23 years', "HS C/o '19", "IWU C/o '23", '2023', 'All of them',
                           'Too Many', '302-555-1234, email@email.com')
        rv = self.app.get('/resumes')
        assert b'Test Name' in rv.data
        assert b'19' in rv.data
        assert b'23 years' in rv.data
        # changed apostrophe to unicode
        assert b'HS C/o &#39;19' in rv.data
        assert b'IWU C/o &#39;23' in rv.data
        assert b'2023' in rv.data
        assert b'All of them' in rv.data
        assert b'Too Many' in rv.data
        assert b'302-555-1234, email@email.com' in rv.data

        self.app.post('/edit_resume', data=dict(
            id=1,
            name='Name Test',
            age='20',
            work_exp='None',
            education_hs='Dropped Out',
            education_college='Harvard',
            graduated='2020',
            skills='Good Lawyer',
            awards='Best Lawyer of 2020',
            contact='Please Don"t'
        ), follow_redirects=True)

        with app.app.app_context():
            db = app.get_db()
            rv = db.execute('SELECT * FROM resume_entries WHERE id=1').fetchone()
        assert 'Test Name' not in rv
        assert '19' not in rv
        assert '23 years' not in rv
        assert "HS C/o '19" not in rv
        assert "IWU C/o '23" not in rv
        assert '2023' not in rv
        assert 'All of them' not in rv
        assert 'Too Many' not in rv
        assert '302-555-1234, email@email.com' not in rv

        assert 'Name Test' in rv
        assert '20' in rv
        assert 'None' in rv
        assert "Dropped Out" in rv
        assert "Harvard" in rv
        assert '2020' in rv
        assert 'Good Lawyer' in rv
        assert 'Best Lawyer of 2020' in rv
        assert 'Please Don"t' in rv


if __name__ == '__main__':
    unittest.main()