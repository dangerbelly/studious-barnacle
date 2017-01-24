import psycopg2
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
import pandas as pd
import csv
from app import db
from config import basedir

def load_table(uploaded_file, tablename):
    #engine = create_engine('postgresql://barnacle:studious@localhost/barnacle')
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    #grade = "grade20"

    #year = "2015"

    #table_name = ('%s-%s' % (grade,year))
    table_name = tablename

    df = pd.read_csv(basedir + "/app/static/%s" % uploaded_file)

    df.to_sql(table_name, engine, if_exists='replace')

class gradelevel_dataset:

	def __init__(self,table):
		engine = create_engine('postgresql://barnacle:studious@localhost/barnacle')
		df = pd.read_sql_query('select * from "%s"' % table, con=engine)
		self.total = len(df.index)

		MAL_list = df['Mathematics Achievement Level']
		MAL_list = list(MAL_list)

		for e, x in enumerate(MAL_list):
			try:
				MAL_list[e] = int(MAL_list[e])
			except (TypeError, ValueError):
				MAL_list[e] = 0

		self.math_4score = sum(1 for x in MAL_list if x==4)
		self.math_3score = sum(1 for x in MAL_list if x==3)
		self.math_2score = sum(1 for x in MAL_list if x==2)
		self.math_1score = sum(1 for x in MAL_list if x==1)

		df2 = pd.DataFrame([['cat','level'],['Standard Exceeded',self.math_4score],['Standard Met',self.math_3score],['Standard Nearly Met',self.math_2score],['Standard Not Met',self.math_1score]])
		df2.to_csv(basedir + '/app/static/data.csv', index=False, header=False)

		EAL_list = df['ELA/Literacy Achievement Level']
		EAL_list = list(EAL_list)

		for e, x in enumerate(EAL_list):
			try:
				EAL_list[e] = int(EAL_list[e])
			except (TypeError, ValueError):
				EAL_list[e] = 0

		self.ela_4score = sum(1 for x in EAL_list if x==4)
		self.ela_3score = sum(1 for x in EAL_list if x==3)
		self.ela_2score = sum(1 for x in EAL_list if x==2)
		self.ela_1score = sum(1 for x in EAL_list if x==1)

		df3 = pd.DataFrame([['cat','level'],['Standard Exceeded',self.ela_4score],['Standard Met',self.ela_3score],['Standard Nearly Met',self.ela_2score],['Standard Not Met',self.ela_1score]])
		df3.to_csv(basedir + '/app/static/data2.csv', index=False, header=False)

class teacherGroup:

	def __init__(self, table1, table2):
		engine = create_engine('postgresql://barnacle:studious@localhost/barnacle')
		df = pd.read_sql_query('select * from "%s"' % table1, con=engine)
		lol = df.values.tolist()

		df_teach = pd.read_sql_query('select * from "%s"' % table2, con=engine)


		teacher_list = df_teach.values.tolist()

		for row, i in enumerate(teacher_list):
			current_ssid = teacher_list[row][1]
			current_teacher = teacher_list[row][2]

			for row, i in enumerate(lol):
				#Turn caaspp data into a string and look for match
				#ssid_caaspp = str(lol[row][3])
				ssid_caaspp = lol[row][3]
				if ssid_caaspp == current_ssid:
					lol[row].append(current_teacher)

		cu_list = []

		for row, i in enumerate(lol):
			try:
				cu_list.append(lol[row][38])
			except IndexError:
				cu_list.append('null')

		df['cu'] = pd.Series(cu_list, index=df.index)

		df.to_sql('masterwithteachers', engine)

		self.df = df

		self.gb = df.groupby('cu')

		self.engine = engine

	def create_group_tables(self):

		engine = self.engine
		gb = self.gb
		df_list = []
		df_groups = []
		for x in gb.groups:
			df_list.append(gb.get_group(x))
			df_groups.append(x)


		for f,b in zip(df_groups, df_list):
			df = b
			name = str(f)
			df.to_sql(name, engine, index=False)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)