from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class DealForm(Form):
    grade = SelectField('Country', choices=[
        ('us','USA'),('gb','Great Britain'),('ru','Russia')])

    year = SelectField('Year', choices=[
        ('1415','14-15'),('1516','15-16'),('1617','16-17')])

#class ClassInfo(Form):
#	classinfo = SelectField('Year', choices=[
#        ('1415','14-15'),('1516','15-16'),('1617','16-17')])

class ClassInfo(Form):
    teachers = ['625','901','421']
    classinfo = SelectField('Year', choices=[(f,f) for f in teachers])

class SelectTeacher(Form):
    teachers = ['625','901','421']
    classinfo = SelectField('Year', choices=[(f,f) for f in teachers])
    result = 'result'

class SelectGradeUpload(Form):
    gradelevels = ['3rd','4th','5th','6th']
    gradeinfo = SelectField('Grade', choices=[(f,f) for f in gradelevels])