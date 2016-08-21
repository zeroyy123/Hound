# -*- coding:utf-8 -*-
import pandas as pd
import MySQLdb as mysql
import numpy as np


class MysqlDriver():
    def __init__(self):
       self.db = mysql.connect(host="127.0.0.1", user="root", passwd="238159", db="hound",charset="utf8")
       self.cursor = self.db.cursor()

    def create_table(self,table_name,df):
        SQL = 'drop table if exists '+table_name
        self.cursor.execute(SQL)

        columns = df.columns
        SQL = 'create table '+table_name+'('
        for i in range(len(columns)):
            type_ = type(df[columns[i]].values[0])
            print type_
            if (type_ is unicode) or (type_ is str):
                SQL = SQL + columns[i]+' varchar(255)'
            elif type_ is np.int64:
                SQL = SQL + columns[i]+' int'
            else:
                SQL = SQL + columns[i]+' float'

            if columns[i] == 'elem_ID':
                SQL = SQL + ' NOT NULL'

            if i < len(columns)-1:
                SQL = SQL + ','
            else:
                SQL = SQL + ')'
        print SQL
        self.cursor.execute(SQL)

    def insert_data(self,table_name,df):
        # 'insert into user values(%s,%s),value
        SQL = 'insert into ' + table_name + ' values('
        columns = df.columns
        df = df.fillna('')
        for j in range(len(columns)):
            if j < len(columns)-1:
                SQL = SQL + '%s,'
            else:
                SQL = SQL + '%s)'
        print SQL
        columns = df.columns
        for i in range(1):
            print i
            print df.values[i]
            self.cursor.execute(SQL,df.values[i])



if __name__ == '__main__':
    name = 'LightsLighting'
    # writer = pd.ExcelWriter(U'F:/GitHub/category/' + name+'.xlsx', engine='xlsxwriter')
    df = pd.read_excel(U'F:/GitHub/category/' + name+'.xlsx','Sheet1',index_col=None,na_values=np.nan)
    del df['Unnamed: 0']
    del df['count']
    del df['elem_ship']
    # df = df[['elem_ID','elem_feedback']]
    # for i in range(len(df.columns)):
    #     print df.columns[i],type(df[df.columns[i]].values[0])
    MD = MysqlDriver()
    MD.create_table(name,df)
    MD.insert_data(name,df)
