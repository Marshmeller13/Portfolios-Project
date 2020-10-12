import os
from flask import Flask, request, g, redirect, url_for, render_template, flash
from sqlite3 import dbapi2 as sqlite3
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

    return render_template('resume_template_orig.html', resume_entries = resume_entries)



@app.route('/create_resume', methods=['POST'])
def create_resume():
    db = get_db()
    db.execute('insert into resume_entries (name, age, work_exp, education_hs, education_college, graduated)',
               [request.form['name'], request.form['age'], request.form['work_exp'], request.form['education_hs'], request.form['education_college'], request.form['graduated']])
    db.commit()
    flash('Resume Successfully Created')
    return redirect(url_for('show_resume'))
