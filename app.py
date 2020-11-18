import os, re
from flask import Flask, request, g, redirect, url_for, render_template, flash, session, make_response
from sqlite3 import dbapi2 as sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


app.config['SECRET_KEY'] = os.urandom(12).hex()

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


@app.route('/show_template')
def show_resume():
    db = get_db()
    refid = session['user_id']
    cur = db.execute('SELECT name, age, work_exp, education_hs, education_college, graduated, skills, awards, contact, id FROM resume_entries WHERE refid=?', (refid,))
    resume_entries = cur.fetchall()

    return render_template('resume_template_orig.html', resume_entries = resume_entries)


@app.route('/create_resume', methods=['POST'])
def create_resume():
    db = get_db()
    user_id = session['user_id']
    db.execute('insert into resume_entries (name, age, work_exp, education_hs, education_college, graduated, skills, awards, contact, refid) values (?,?,?,?,?,?,?,?,?,?)',
               [request.form['name'], request.form['age'], request.form['work_exp'], request.form['education_hs'], request.form['education_college'], request.form['graduated'], request.form['skills'], request.form['awards'], request.form['contact'], int(user_id,)])
    db.commit()
    flash('Resume Successfully Created')
    return redirect(url_for('display_resumes'))


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
        use_id = user['id']
        #if statement for if username matches any users, then checks password associated with account
        if user is None:
            error = 'Username does not exist!'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        #if no errors encountered, redirect to homepage/dashboard (with framework for setting up a session id within cookies of browser)
        if error is None:
            session.clear()
            session['user_id'] = use_id

            current = db.execute('SELECT name, user_id FROM profiles WHERE user_id=?', (use_id,))
            profiles = current.fetchone()
            try:
                if profiles['user_id']:
                    return redirect(url_for('profile_page'))
                else:
                    return redirect(url_for('profile_form'))

            except TypeError:
                return redirect(url_for('profile_form'))






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
        sqlite_insert_blob_query = """ INSERT INTO uploaded_resumes(resume, position, user_id) VALUES (?, ?, ?)"""
        resume = request.files['file']
        resume = convertToBinaryData(resume)
        position = request.form['position']
        user_id = session['user_id']
        # Convert data into tuple format
        data_tuple = (resume, position, int(user_id,))
        db.execute(sqlite_insert_blob_query, data_tuple)
        db.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        db.close()
        return redirect(url_for('show_profile'))

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

                flash('Account Created!')
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


@app.route('/profile_page', methods=['GET'])
def profile_page():

    user_id = session['user_id']
    db = get_db()
    cur = db.execute('SELECT id, name, theme, profile_pic, job, school1, school1_info, school2, school2_info, school3, school3_info, language1, language2, language3, language4, language5, language6, language7, exp1, company1, dur1, desc1, exp2, company2, dur2, desc2, address, phone, email, website FROM profiles WHERE user_id=?', (user_id,))
    profiles = cur.fetchone()
    if profiles['theme']:
        theme = str(profiles['theme'])
        if theme == "blue":
            return render_template('profile_page_blue.html', profiles=profiles)
        elif theme == "red":
            return render_template('profile_page_red.html', profiles=profiles)
        elif theme == "green":
            return render_template('profile_page_green.html', profiles=profiles)
        elif theme == "teal":
            return render_template('profile_page_teal.html', profiles=profiles)
    else:
        return render_template('profile_page_blue.html', profiles=profiles)



"redirects user to profile page"
@app.route('/profile_page_blue')
def show_profile_blue():

    user_id = session['user_id']
    db = get_db()
    cur = db.execute('SELECT id, theme, name, profile_pic, job, school1, school1_info, school2, school2_info, school3, school3_info, language1, language2, language3, language4, language5, language6, language7, exp1, company1, dur1, desc1, exp2, company2, dur2, desc2, address, phone, email, website FROM profiles WHERE user_id=?', (user_id,))
    profiles = cur.fetchone()
    make_pic(profiles['profile_pic'])
    return render_template('profile_page_blue.html', profiles=profiles)





@app.route('/profile_page_red')
def show_profile_red():

    user_id = session['user_id']
    db = get_db()
    cur = db.execute('SELECT id, theme, name, profile_pic, job, school1, school1_info, school2, school2_info, school3, school3_info, language1, language2, language3, language4, language5, language6, language7, exp1, company1, dur1, desc1, exp2, company2, dur2, desc2, address, phone, email, website FROM profiles WHERE user_id=?', (user_id,))
    profiles = cur.fetchone()
    make_pic(profiles['profile_pic'])
    return render_template('profile_page_red.html', profiles=profiles)


@app.route('/profile_page_green')
def show_profile_green():

    user_id = session['user_id']
    db = get_db()
    cur = db.execute('SELECT id, name, theme, profile_pic, job, school1, school1_info, school2, school2_info, school3, school3_info, language1, language2, language3, language4, language5, language6, language7, exp1, company1, dur1, desc1, exp2, company2, dur2, desc2, address, phone, email, website FROM profiles WHERE user_id=?', (user_id,))
    profiles = cur.fetchone()
    make_pic(profiles['profile_pic'])
    return render_template('profile_page_green.html', profiles=profiles)


@app.route('/profile_page_teal')
def show_profile_teal():

    user_id = session['user_id']
    db = get_db()
    cur = db.execute('SELECT id, name, theme, profile_pic, job, school1, school1_info, school2, school2_info, school3, school3_info, language1, language2, language3, language4, language5, language6, language7, exp1, company1, dur1, desc1, exp2, company2, dur2, desc2, address, phone, email, website FROM profiles WHERE user_id=?', (user_id,))
    profiles = cur.fetchone()
    make_pic(profiles['profile_pic'])
    return render_template('profile_page_teal.html', profiles=profiles)


@app.route('/resumes')
def display_resumes():

    user_id = session['user_id']
    db = get_db()
    cur = db.execute('SELECT name, age, work_exp, education_hs, education_college, graduated, skills, awards, contact, id FROM resume_entries WHERE refid=?', (user_id,))
    resume_entries = cur.fetchall()
    return render_template('posts_page.html', resume_entries=resume_entries)


@app.route('/edit_resume', methods=['POST'])
def edit_resume():
    db = get_db()
    db.execute("UPDATE resume_entries SET name=?, age=?, work_exp=?, education_hs=?, education_college=?, graduated=?, skills=?, awards=?, contact=? WHERE id=?",
               [request.form['name'], request.form['age'], request.form['work_exp'], request.form['education_hs'], request.form['education_college'], request.form['graduated'], request.form['skills'], request.form['awards'], request.form['contact'], request.form['id']])
    db.commit()
    flash('Entry was Successfully Edited')
    return redirect(url_for('display_resumes'))


@app.route('/edit_page', methods=['GET', 'POST'])
def edit_form():
    db = get_db()

    current = db.execute('SELECT name, age, work_exp, education_hs, education_college, graduated, skills, awards, contact, id FROM resume_entries WHERE id=?',
                         [request.args['id']])
    resume_entries = current.fetchall()

    return render_template('edit_resume.html', resume_entries=resume_entries)


@app.route('/get_blob', methods=['GET'])
def get_blob(id):
    db = get_db()
    user_id = session['user_id']
    cur = db.execute('SELECT resume FROM uploaded_resumes WHERE user_id=?', (user_id,))
    uploaded_resumes = cur.fetchone()
    up_resume = uploaded_resumes['resume']

    return up_resume


@app.route('/docs/<id>')
def make_pdf(id=None):
    if id is not None:
        pdf_res = get_blob(id)
        response = make_response(pdf_res)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'pdf_upload'

        return response


@app.route('/<id>')
def display_uploaded(id=None):

    return render_template('display_uploaded.html', id=id)


@app.route('/uploaded_list')
def uploaded_list():


    user_id = int(session['user_id'])
    db = get_db()
    cur = db.execute('SELECT position, id FROM uploaded_resumes WHERE user_id=?', (user_id,))
    uploaded_resumes = cur.fetchall()
    return render_template('uploaded_list.html', uploaded_resumes=uploaded_resumes)


@app.route('/delete_uploaded', methods=['POST'])
def delete_uploaded():
    db = get_db()
    db.execute('delete from uploaded_resumes where id = ?',
               [request.form['delete']])
    db.commit()

    flash('Resume was successfully deleted!')
    return redirect(url_for('uploaded_list'))


@app.route('/profile_form', methods=['GET', 'POST'])
def profile_form():
    db = get_db()
    user_id = session['user_id']
    current = db.execute('SELECT name, theme, profile_pic, job, school1, school1_info, school2, school2_info, school3, school3_info, language1, language2, language3, language4, language5, language6, language7, exp1, company1, dur1, desc1, exp2, company2, dur2, desc2, address, phone, email, website FROM profiles WHERE user_id=?',(user_id,))
    profiles = current.fetchone()

    return render_template('create_profile.html', profiles=profiles)


@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    db = get_db()
    user_id = session['user_id']
    profile_pic = request.files['file']
    profile_pic = convertToBinaryData(profile_pic)

    current = db.execute('SELECT name, theme, profile_pic, job, school1, school1_info, school2, school2_info, school3, school3_info, language1, language2, language3, language4, language5, language6, language7, exp1, company1, dur1, desc1, exp2, company2, dur2, desc2, address, phone, email, website FROM profiles WHERE user_id=?',(user_id,))
    profiles = current.fetchone()
    try:
        if not request.form['theme']:
            if not profiles['theme']:
                theme = 'blue'
            else:
                theme = profiles['theme']
        else:
            theme = str(request.form['theme'])
    except KeyError:
        theme = profiles['theme']

    db.execute("UPDATE profiles SET name=?, theme=?, profile_pic=?, job=?, school1=?, school1_info=?, school2=?, school2_info=?, school3=?, school3_info=?, language1=?, language2=?, language3=?, language4=?, language5=?, language6=?, language7=?, exp1=?, company1=?, dur1=?, desc1=?, exp2=?, company2=?, dur2=?, desc2=?, address=?, phone=?, email=?, website=? WHERE user_id=?",
               [request.form['name'], theme, profile_pic, request.form['job'], request.form['school1'], request.form['school1_info'], request.form['school2'], request.form['school2_info'], request.form['school3'], request.form['school3_info'], request.form['language1'], request.form['language2'], request.form['language3'], request.form['language4'], request.form['language5'], request.form['language6'], request.form['language7'],
                request.form['exp1'], request.form['company1'], request.form['dur1'], request.form['desc1'], request.form['exp2'], request.form['company2'], request.form['dur2'], request.form['desc2'], request.form['address'], request.form['phone'], request.form['email'], request.form['website'], int(user_id,)])
    db.commit()
    return redirect(url_for('profile_page'))


@app.route('/edit_profile_form', methods=['GET', 'POST'])
def edit_profile_form():
    db = get_db()

    user_id = int(session['user_id'])
    current = db.execute('SELECT name, id, theme, profile_pic, job, school1, school1_info, school2, school2_info, school3, school3_info, language1, language2, language3, language4, language5, language6, language7, exp1, company1, dur1, desc1, exp2, company2, dur2, desc2, address, phone, email, website FROM profiles WHERE user_id=?', (user_id,))
    profiles = current.fetchone()
    make_pic(profiles['id'])

    return render_template('edit_profile.html', profiles=profiles)


@app.route('/create_profile', methods=['POST'])
def create_profile():
    db = get_db()
    user_id = session['user_id']
    profile_pic = request.files['file']
    profile_pic = convertToBinaryData(profile_pic)
    sqlite_insert_blob_query = """ INSERT INTO profiles(name, theme, profile_pic, user_id, job, school1, school1_info, school2, school2_info, school3, school3_info, language1, language2, language3, language4, language5, language6, language7, exp1, company1, dur1, desc1, exp2, company2, dur2, desc2, address, phone, email, website ) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

    try:
        if not request.form['theme']:
                theme = 'blue'

        else:
            theme = str(request.form['theme'])
    except KeyError:
        theme = 'blue'

    data_tuple = (request.form['name'], theme, profile_pic, int(user_id,), request.form['job'], request.form['school1'], request.form['school1_info'], request.form['school2'], request.form['school2_info'], request.form['school3'], request.form['school3_info'],
                request.form['language1'], request.form['language2'], request.form['language3'], request.form['language4'], request.form['language5'], request.form['language6'], request.form['language7'],
                request.form['exp1'], request.form['company1'], request.form['dur1'], request.form['desc1'], request.form['exp2'], request.form['company2'], request.form['dur2'], request.form['desc2'], request.form['address'], request.form['phone'], request.form['email'],
                request.form['website'])
    db.execute(sqlite_insert_blob_query, data_tuple)

    db.commit()
    db.close()
    return redirect(url_for('profile_page'))

@app.route('/get_pic', methods=['GET'])
def get_pic(id):
    db = get_db()
    user_id = session['user_id']
    cur = db.execute('SELECT profile_pic FROM profiles WHERE user_id=?', (user_id,))
    profile = cur.fetchone()
    pic = profile['profile_pic']

    return pic


@app.route('/docs/pic<id>')
def make_pic(id=None):
    if id is not None:
        pic_res = get_pic(id)
        response = make_response(pic_res)
        response.headers['Content-Type'] = 'image/png'
        response.headers['Content-Disposition'] = 'inline; filename=%s.png' % 'pdf_upload'

        return response

