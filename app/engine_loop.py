import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import csv

engine = create_engine('postgresql://barnacle:studious@localhost/barnacle')

df = pd.read_sql_query('select * from "us-1415-teachers"', con=engine)

lol = df.values.tolist()

with open('/home/dangerbelly/microblog/app/cid_cu.csv') as f:
    reader = csv.reader(f)
    teacher_list = [row for row in reader]

for row, i in enumerate(teacher_list):
    current_ssid = teacher_list[row][0]
    current_teacher = teacher_list[row][1]

    for row, i in enumerate(lol):
        #Turn caaspp data into a string and look for match
        ssid_caaspp = str(lol[row][3])
        if ssid_caaspp == current_ssid:
            lol[row].append(current_teacher)

cu_list = []

for row, i in enumerate(lol):
	try:
		cu_list.append(lol[row][39])
	except IndexError:
		cu_list.append('null')