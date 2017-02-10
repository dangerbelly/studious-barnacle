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

def fill_total_entry(this_table, this_school):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    df = pd.read_sql_query('select * from "%s"' % this_table, con=engine)
    per_sch_count = df[df['Enrolled School'] == this_school].count()['Student ID']
    per_sch_male = df[(df['Enrolled School'] == this_school) & (df['Gender'] == 'M')].count()['Student ID']
    per_sch_female = df[(df['Enrolled School'] == this_school) & (df['Gender'] == 'F')].count()['Student ID']
    per_sch_lim_eng = df[(df['Enrolled School'] == this_school) & (df['Limited English Proficiency Status'] == 'Y')].count()['Student ID']
    unique_lang_code = df['Language Code'].unique()
    language_dict = {}
    for language in unique_lang_code:
        count = df[(df['Enrolled School'] == this_school) & (df['Language Code'] == language)].count()['Student ID']
        language_dict[language] = count

    count_list = [per_sch_count, per_sch_male, per_sch_female, per_sch_lim_eng, language_dict]

    return count_list

#def display_summary(this_grade_year):
#	engine = create_engine(SQLALCHEMY_DATABASE_URI)
#	data_unit = StudentCounts.query.filter_by(school=this_grade_year).first()
#	this_stu_total = data_unit.total_stu_count
#	data_to_return = {'total_count':this_stu_total}
#	return data_to_return

def load_stu_counts(this_grade_year):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    this_table = "table_" + this_grade_year
    df = pd.read_sql_query('select * from "%s"' % this_table, con=engine)
    this_total_count = len(df.index)
    total_entry = StudentCounts(school=this_grade_year, total_stu_count=this_total_count)
    db.session.add(total_entry)
    db.session.commit()

def fill_dropdown(unique_list):
    unique = UniqueSchools()
    for x in unique_list:
        unique.AddSchool(x)