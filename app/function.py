import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.automap import automap_base
from config import SQLALCHEMY_DATABASE_URI
import pandas as pd
import csv
from app import db
from config import basedir
from .models import StudentCounts

def calc_limited_eng_prof(this_table):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    df = pd.read_sql_query('select * from "%s"' % this_table, con=engine)
    df = df['Limited English Proficiency Status']
    lim_eng_list = df.tolist()
    yes = sum(1 for x in lim_eng_list if x=='Y')
    no = df.isnull().sum()
    yesno = [yes,no]
    return yesno

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
