import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import csv

engine = create_engine('postgresql://barnacle:studious@localhost/barnacle')

df = pd.read_sql_query('select * from "us-1415-teachers"', con=engine)