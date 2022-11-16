import pandas as pd
import sqlite3, sys

file_sqlite3=sys.argv[1]
conn = sqlite3.connect(file_sqlite3)
df=pd.read_sql_query('SELECT * FROM ESA', conn)

#print(df.columns)
for index,row in df.iterrows():
    print("%s-%s %s" % (row['puckid'],row['pinid'],row['sample_name']))
