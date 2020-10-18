import os
from flask import Flask, request, g, redirect, url_for, render_template, flash, session
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

@app.route('/')
def show_resume():
    db = get_db()
    cur = db.execute('SELECT id, name, age, work_exp, education_hs, education_college, graduated FROM resume_entries ORDER BY id DESC')
    resume_entries = cur.fetchall()

    return render_template('login.html', resume_entries = resume_entries)



@app.route('/create_resume', methods=['POST'])
def create_resume():
    db = get_db()
    db.execute('insert into resume_entries (name, age, work_exp, education_hs, education_college, graduated)',
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
            error = 'Incorrect username.'
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

