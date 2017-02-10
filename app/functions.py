import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.automap import automap_base
from config import SQLALCHEMY_DATABASE_URI
import pandas as pd
import csv
from app import db
from config import basedir
from .models import StudentCounts, UniqueSchools

def calc_limited_eng_prof(this_table):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    df = pd.read_sql_query('select * from "%s"' % this_table, con=engine)
    df = df['Limited English Proficiency Status']
    lim_eng_list = df.tolist()
    yes = sum(1 for x in lim_eng_list if x=='Y')
    no = df.isnull().sum()
    yesno = [yes,no]
    return yesno

def get_unique_school_names(this_table):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    df = pd.read_sql_query('select * from "%s"' % this_table, con=engine)
    u = df['Enrolled School'].unique()
    u = list(u)
    return u

def fill_dropdown(unique_list):
    unique = UniqueSchools()
    for x in unique_list:
        unique.AddSchool(x)

def fill_total_entry(this_table, a_list):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    df = pd.read_sql_query('select * from "%s"' % this_table, con=engine)
    for this_school in a_list:
        per_sch_count = int(df[df['Enrolled School'] == this_school].count(level=None)['Student ID'])
        per_sch_male = int(df[(df['Enrolled School'] == this_school) & (df['Gender'] == 'M')].count(level=None)['Student ID'])
        per_sch_female = int(df[(df['Enrolled School'] == this_school) & (df['Gender'] == 'F')].count(level=None)['Student ID'])
        per_sch_lim_eng = int(df[(df['Enrolled School'] == this_school) & (df['Limited English Proficiency Status'] == 'Y')].count(level=None)['Student ID'])
        unique_lang_code = df['Language Code'].unique()
        language_dict = {}
        for language in unique_lang_code:
            count = int(df[(df['Enrolled School'] == this_school) & (df['Language Code'] == language)].count(level=None)['Student ID'])
            language_dict[language] = count

        #per_sch_count = int(per_sch_count)

        count_list = [per_sch_count, per_sch_male, per_sch_female, per_sch_lim_eng, language_dict]

        this_row = StudentCounts(school=this_school, total_stu_count=per_sch_count, male_count=per_sch_male, female_count=per_sch_female, lim_eng_yes=per_sch_lim_eng)
        db.session.add(this_row)

    return "OK"

#def display_summary(this_grade_year):
#	engine = create_engine(SQLALCHEMY_DATABASE_URI)
#	data_unit = StudentCounts.query.filter_by(school=this_grade_year).first()
#	this_stu_total = data_unit.total_stu_count
#	data_to_return = {'total_count':this_stu_total}
#	return data_to_return

#def load_stu_counts(this_grade_year):
#    engine = create_engine(SQLALCHEMY_DATABASE_URI)
#    this_table = "table_" + this_grade_year
#    df = pd.read_sql_query('select * from "%s"' % this_table, con=engine)
#    this_total_count = len(df.index)
#    total_entry = StudentCounts(school=this_grade_year, total_stu_count=this_total_count)
#    db.session.add(total_entry)
#    db.session.commit()

