import psycopg2
from sqlalchemy import create_engine
import pandas as pd

def load_table(uploaded_file):
    engine = create_engine('postgresql://barnacle:studious@localhost/barnacle')

    grade = "grade20"

    year = "2015"

    table_name = ('%s-%s' % (grade,year))

    df = pd.read_csv("/home/dangerbelly/microblog/app/static/%s" % uploaded_file)

    df.to_sql(table_name, engine)

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
		df2.to_csv('/home/dangerbelly/microblog/app/static/data.csv', index=False, header=False)

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
		df3.to_csv('/home/dangerbelly/microblog/app/static/data2.csv', index=False, header=False)