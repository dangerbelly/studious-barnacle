import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import csv


class teacherGroup:

	def __init__(self, table1, table2):
		engine = create_engine('postgresql://barnacle:studious@localhost/barnacle')
		df = pd.read_sql_query('select * from "%s"' % table1, con=engine)
		self.total = len(df.index)

		lol = df.values.tolist()

		df_teach = pd.read_sql_query('select * from "%s"' % table2, con=engine)
		self.total = len(df.index)

		teacher_list = list(df_teach)

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

		df['cu'] = pd.Series(cu_list, index=df.index)

		df.to_sql('masterwteachers', engine)

		self.df = df