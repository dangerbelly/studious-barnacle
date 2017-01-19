from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
from .forms import DealForm
from .forms import ClassInfo
from .models import load_table
from .models import teacherGroup
from .models import gradelevel_dataset
from werkzeug import secure_filename
import os

app.config['UPLOAD_FOLDER'] = '/static'

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


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

@app.route('/deal', methods=['GET', 'POST'])
def deal():
    form = DealForm()
#    if not form.validate_on_submit():
#        flash('Country selected="%s"' % (form.Country.data))
#        return redirect('/index')
#        #return render_template( 'deal.html', user='ryan', form = form)
#    else:
#        return render_template( 'deal.html', form = form )

    if form.validate_on_submit():
        flash('Country selected="%s" Year selected"%s"' % (form.grade.data,form.year.data))
        load_table(form.grade.data,form.year.data)
        return redirect('/index')

    return render_template( 'deal.html', user='ryan', form = form)

def year():
    form = YearForm()
#    if not form.validate_on_submit():
#        flash('Country selected="%s"' % (form.Country.data))
#        return redirect('/index')
#        #return render_template( 'deal.html', user='ryan', form = form)
#    else:
#        return render_template( 'deal.html', form = form )

    if form.validate_on_submit():
        flash('Year selected="%s"' % (form.year.data))
        return redirect('/index')
    return render_template( 'deal.html', user='ryan', form = form)

@app.route('/classinfo', methods=['GET', 'POST'])
def classinfo():
    form = ClassInfo()

    if form.validate_on_submit():
        return redirect('/index')
    return render_template('classinfo.html', user='ryan', form =form)


@app.route('/uploader', methods=['GET', 'POST'])
def upload():
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

        load_table(filename, "master1")

        gld = gradelevel_dataset('master1')

        #return render_template('classinfo.html', user='ryan', form=form, filename=filename)
        return redirect('/classinfo')

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
        return redirect('/classinfo')


@app.route('/teacherdropdown', methods=['GET', 'POST'])
def teacherdropdown():
    form = TeacherDropdown()


    if form.validate_on_submit():
        return redirect('/index')
    return redirect('/classinfo')

@app.route('/uploads')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/example', methods=['GET', 'POST'])
def example():
    return render_template('example.html')

