from flask_wtf import FlaskForm as BaseForm
from wtforms import StringField, BooleanField, SelectField, SelectMultipleField, TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from .models import UniqueSchools


class LoginForm(BaseForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class DealForm(BaseForm):
    grade = SelectField('Country', choices=[
        ('us','USA'),('gb','Great Britain'),('ru','Russia')])

    year = SelectField('Year', choices=[
        ('1415','14-15'),('1516','15-16'),('1617','16-17')])

#class ClassInfo(Form):
#	classinfo = SelectField('Year', choices=[
#        ('1415','14-15'),('1516','15-16'),('1617','16-17')])

class SimpleForm(BaseForm):
    content = TextField('content')

class ClassInfo(BaseForm):
    teachers = ['625','901','421']
    classinfo = SelectField('Year', choices=[(f,f) for f in teachers])

class SelectTeacher(BaseForm):
    teachers = ['625','901','421']
    classinfo = SelectField('Year', choices=[(f,f) for f in teachers])
    result = 'result'

class SelectGradeUpload(BaseForm):
    gradelevels = ['3rd','4th','5th','6th']
    gradeinfo = SelectField('Grade', choices=[(f,f) for f in gradelevels])

class PreviewData(BaseForm):
    def fill_field():
        return UniqueSchools.query.all()

    myfield = QuerySelectField(query_factory=fill_field)