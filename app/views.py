from flask import render_template, flash, redirect, request, jsonify
from app import app, models, db
from .forms import LoginForm
from .forms import DealForm
from .forms import ClassInfo
from .forms import SelectTeacher
from .models import load_table
from .models import teacherGroup
from .models import gradelevel_dataset
from .models import User
from .models import UniqueSchools
from .function import calc_limited_eng_prof
from config import basedir
from werkzeug import secure_filename
import os
import json

#APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static')
UPLOAD_FOLDER = basedir + '/app/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')


@app.route('/index', methods=['GET', 'POST'])
def classinfo():
    form = ClassInfo()

    #user1_obj = User.query.get(1)
    #user1_dict = user1_obj.__dict__
    #user1 = user1_dict['nickname']
    user1='ryan'

    if form.validate_on_submit():
        return redirect('/index')
    return render_template('index.html', user='ryan', form =form, user1=user1)


@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    form = ClassInfo()
    # Get the name of the uploaded file
    file = request.files['file']

    grade_value = (request.form.get('grade_value'))
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)

        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        load_table(filename, "master1_%s" % grade_value)

        gld = gradelevel_dataset('master1_%s' % grade_value)

        return redirect('/index#initialize')

@app.route('/test', methods=['GET', 'POST'])
def test():
   
    if request.method == 'POST':
        value_one = int(request.form.get('first'))
        file = (request.form.get('file'))
        grade_value = (request.form.get('grade_value'))
        data = {"total_students":1562,"school_number":2,"schools":'RL, JX'}

        print(grade_value)
        #return jsonify(data)
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)

            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            load_table(filename, "master1_%s" % grade_value)

            gld = gradelevel_dataset('master1_%s' % grade_value)

            #return redirect('/index#initialize')
            return jsonify(data)
    return redirect('/index#anchor2')

@app.route('/test2', methods=['POST'])
def test2():
    if request.method == 'POST':
        file = request.files['file']
        grade_upload = request.form.get('gradeupload')
        year_upload = request.form.get('yearupload')
        print(grade_upload)
        print(year_upload)
        #test_dict = dict(test)
        #print(test_dict)
        #print(test_dict['file'])
        print("foobar")
        #text_var = request.form.get('text')
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)

            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            tablename = "table_%s_%s" % (grade_upload,year_upload)
            load_table(filename, "table_%s_%s" % (grade_upload,year_upload))

            gld = gradelevel_dataset('table_%s_%s' % (grade_upload,year_upload))

            u = models.UniqueSchools(school='JX Wilson')
            db.session.add(u)
            db.session.commit()

            test_school_list = ['Robert L. Stevens Elementary', 'Wright Charter', 'J. X. Wilson Elementary']
            for row,x in enumerate(test_school_list):
                this_school = test_school_list[row]
                u = models.UniqueSchools(school=this_school)
                db.session.add(u)
            db.session.commit()

            count = calc_limited_eng_prof(tablename)
            print(count)

        return redirect('/index#anchor2')
    return redirect('/index#initialize')


@app.route('/group_by', methods=['GET', 'POST'])
def group_by():
    form = ClassInfo()
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        load_table(filename, "teachertable")

        tg = teacherGroup('master1','teachertable')

        tg.create_group_tables( )

        #return render_template('classinfo.html', user='ryan', form=form, filename=filename)
        return redirect('/index')


@app.route('/teacherdropdown', methods=['GET', 'POST'])
def teacherdropdown():
    form = TeacherDropdown()


    if form.validate_on_submit():
        return redirect('/index')
    return redirect('/classinfo')

@app.route('/selectateacher', methods=['GET', 'POST'])
def selectateacher():
    form = SelectTeacher()

    if form.validate_on_submit():
        return redirect('/index#anchor2', result=result)
    return redirect('/index')

@app.route('/uploads')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/example', methods=['GET', 'POST'])
def example():
    return render_template('example.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        load_table(grade)
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
