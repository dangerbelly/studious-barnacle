from flask import render_template, flash, redirect, request, jsonify
from app import app, models, db
from .forms import LoginForm
from .forms import DealForm
from .forms import ClassInfo
from .forms import SelectTeacher
from .forms import PreviewData
from .forms import SimpleForm
from .models import load_table
from .models import teacherGroup
from .models import gradelevel_dataset
from .models import User
from .models import UniqueSchools
from .models import StudentCounts
from .functions import calc_limited_eng_prof
from .functions import fill_dropdown, get_unique_school_names, fill_total_entry
from .models import mst, e
#from .function import display_summary
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
    form2 = PreviewData()
    #user1_obj = User.query.get(1)
    #user1_dict = user1_obj.__dict__
    #user1 = user1_dict['nickname']
    user1='ryan'
    #how_many = StudentCounts.query.filter_by(school='Wright Charter').first()
    #total_stu = how_many.total_stu_count
    total_stu=150
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('index.html', user='ryan', form =form, user1=user1, total_stu=total_stu,form2=form2)

@app.route('/test1', methods=['POST'])
def test1():
    if request.method == 'POST':
        test_var = 'test'
        print(test_var)
    return redirect('/index')

@app.route('/display')
def display():
    return redirect('/index')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        grade_upload = request.form.get('gradeupload')
        year_upload = request.form.get('yearupload')
        print(grade_upload)
        print(year_upload)
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

            #Look through newly entered data and add any new schools to the dropdown
            this_list = get_unique_school_names(tablename)
            fill_dropdown(this_list)
            fill_total_entry(tablename, this_list)

            
            #display_data = display_summary(grade_upload + "_" + year_upload)
            #print(mst.__dict__)
            #print(mst.columns.keys())   
            print(e)

            #wc_counts = fill_total_entry(tablename, 'Wright Charter')
            #print(wc_counts)

            db.session.commit()




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
