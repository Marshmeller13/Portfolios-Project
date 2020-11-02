import os, re
from flask import Flask, request, g, redirect, url_for, render_template, flash, session, make_response
from sqlite3 import dbapi2 as sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


"Makes /login default page for site"
@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/show_resume')
def show_resume():
    db = get_db()
    cur = db.execute('SELECT name, age, work_exp, education_hs, education_college, graduated, id FROM resume_entries')
    resume_entries = cur.fetchall()

    return render_template('resume_template_orig.html', resume_entries = resume_entries)


@app.route('/create_resume', methods=['POST'])
def create_resume():
    db = get_db()
    db.execute('insert into resume_entries (name, age, work_exp, education_hs, education_college, graduated) values (?,?,?,?,?,?)',
               [request.form['name'], request.form['age'], request.form['work_exp'], request.form['education_hs'], request.form['education_college'], request.form['graduated']])
    db.commit()
    flash('Resume Successfully Created')
    return redirect(url_for('show_resume'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        #get submitted username and password
        username = request.form['username']
        password = request.form['password']

        #set error to none to be changed if program encounters an error
        error = None

        #query database for username
        db = get_db()
        user = db.execute('select * from user where username = ?', (username,)).fetchone()

        #if statement for if username matches any users, then checks password associated with account
        if user is None:
            error = "Username doesn't exist!"
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        #if no errors encountered, redirect to homepage/dashboard (with framework for setting up a session id within cookies of browser)
        if error is None:
            #session.clear()
            #session['user_id'] = user['id']
            return render_template('resume_template_orig.html')

        #flash error encountered (if any)
        flash(error)

    return render_template('login.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')

def convertToBinaryData(file):
    #Convert digital data to binary format


    blobData = request.files['file'].read()

    return blobData


app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024


@app.route('/insert_resume', methods=['GET', 'POST'])
def insert_resume():
    try:
        db = get_db()
        sqlite_insert_blob_query = """ INSERT INTO uploaded_resumes
                                  (resume) VALUES (?)"""
        resume = request.files['file']
        resume = convertToBinaryData(resume)
        # Convert data into tuple format
        data_tuple = (resume,)
        db.execute(sqlite_insert_blob_query, data_tuple)
        db.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        db.close()
        return render_template('resume_template_orig.html')

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (db):
            db.close()


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        ##get inputs for account
        username = request.form['username']
        password = request.form['password']
        confirmpass = request.form['confirmpassword']

        ##set up for unique username validation
        db = get_db()
        user = db.execute('select * from user where username = ?', (username,)).fetchone()

        ##username validation
        if user is None:
            ##check confirmpassword for if it matches password and password is 8 characters long
            if confirmpass != password:
                flash('Passwords do not match!')
            elif len(password) < 8:
                flash('Password must be more than 8 characters.')

            ##insertion of account into database
            else:
                #hash password
                hashedpass = generate_password_hash(password)

                db.execute('INSERT INTO user(username,password) VALUES(?,?)', (username, hashedpass))
                db.commit()

                return render_template('login.html')
        else:
            flash('Username is already taken.')

    return render_template('signup.html')
  
  
@app.route('/delete_resume', methods=['POST'])
def delete_resume():
    db = get_db()
    db.execute('delete from resume_entries where id = ?',
               [request.form['delete']])
    db.commit()

    flash('Resume was successfully deleted!')
    return redirect(url_for('display_resumes'))


"redirects user to profile page"
@app.route('/profile_page')
def show_profile():
    return render_template('profile_page.html')


@app.route('/resumes')
def display_resumes():
    db = get_db()
    cur = db.execute('SELECT name, age, work_exp, education_hs, education_college, graduated, id FROM resume_entries')
    resume_entries = cur.fetchall()
    return render_template('posts_page.html', resume_entries=resume_entries)


@app.route('/edit_resume', methods=['POST'])
def edit_resume():
    db = get_db()
    db.execute("UPDATE resume_entries SET name=?, age=?, work_exp=?, education_hs=?, education_college=?, graduated=? WHERE id=?",
               [request.form['name'], request.form['age'], request.form['work_exp'], request.form['education_hs'], request.form['education_college'], request.form['graduated'], request.form['id']])
    db.commit()
    flash('Entry was Successfully Edited')
    return redirect(url_for('display_resumes'))


@app.route('/edit_page', methods=['GET', 'POST'])
def edit_form():
    db = get_db()

    current = db.execute('SELECT name, age, work_exp, education_hs, education_college, graduated, id FROM resume_entries WHERE id=?',
                         [request.args['id']])
    resume_entries = current.fetchall()

    return render_template('edit_resume.html', resume_entries=resume_entries)


def get_blob(id):
    db = get_db()
    cur = db.execute('SELECT resume, id FROM uploaded_resumes WHERE id=?',
                     [request.args['id']])
    uploaded_resumes = cur.fetchall()

    return uploaded_resumes
