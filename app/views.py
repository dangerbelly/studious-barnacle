from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
from .forms import DealForm
from .forms import ClassInfo
from .models import load_table

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

@app.route('/example', methods=['GET', 'POST'])
def example():
    return render_template('example.html')

