import pandas as pd
from sqlalchemy import create_engine

# 创建数据库引擎
engine = create_engine("mysql+pymysql://root:Llb011223@localhost:3306/agricultureDB?charset=utf8")

# 读入农业数据
df = pd.read_csv('./data_agriculture.csv',sep='\t',encoding='utf-8')

# 存入数据库
df.to_sql('agriculture', con=engine, if_exists='append', index=False)

# 读入气候数据
df = pd.read_csv('./data_meteorology.csv',sep='\t',encoding='utf-8')

# 存入数据库
df.to_sql('meteorology', con=engine, if_exists='append', index=False)
