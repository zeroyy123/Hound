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
        df = df.dropna()
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
        for i in range(len(columns)):
            temp = df[columns[i]]
            temp = temp.dropna()
            if (type(temp.values[0]) is unicode) or (type(temp.values[0]) is str):
                df[columns[i]] = df[columns[i]].fillna('')
            else:
                df[columns[i]] = df[columns[i]].fillna(0)
        for j in range(len(columns)):
            if j < len(columns)-1:
                SQL = SQL + '%s,'
            else:
                SQL = SQL + '%s)'
        print SQL


        temp = df.values.tolist()
        print len(temp)

        print type(temp)
        print 'writing...'

        delta = 10000
        l1 = len(temp)/delta
        l2 = len(temp)%delta
        for i in range(l1):
            print i
            self.cursor.executemany(SQL,temp[i*delta:(i+1)*delta])
        self.cursor.executemany(SQL,temp[l1*delta:len(temp)])
        # for i in range(len(df)):
        #     if i % 100 == 0:
        #         print i
        #     # print df.values[i]
        #     self.cursor.execute(SQL,df.values[i])


def get_name():
    df = pd.read_csv(U'F:/GitHub/Hound_data/item_list.csv')
    df = df.fillna('')

    L = len(df)
    item_catepory = []
    for i in range(L):
        catepory = (df['cate_1'].values)[i]
        catepory = catepory.replace(' ','')
        catepory = catepory.replace("'",'')
        catepory = catepory.replace('&','')
        catepory = catepory.replace('/','_')
        catepory = catepory.replace('"','')
        catepory = catepory.replace('*','x')
        catepory = catepory.replace('<','')
        catepory = catepory.replace('>','')
        item_catepory.append(catepory)

    dout = []
    for i in range(len(item_catepory)):
        if i == 0:
            dout.append(item_catepory[i])
        elif item_catepory[i] != item_catepory[i-1]:
            dout.append(item_catepory[i])
    return dout

if __name__ == '__main__':
    names = get_name()
    print names

    MD = MysqlDriver()
    for n in range(8,len(names),1):
        name = names[n]
        print name
        # writer = pd.ExcelWriter(U'F:/GitHub/category/' + name+'.xlsx', engine='xlsxwriter')

        try:
            df = pd.read_excel(U'F:/GitHub/category/' + name+'.xlsx','Sheet1',index_col=None,na_values=np.nan)
        except:
            df = pd.read_excel(U'F:/GitHub/category/' + name+'_1.xlsx','Sheet1',index_col=None,na_values=np.nan)
            df = df.append(pd.read_excel(U'F:/GitHub/category/' + name+'_2.xlsx','Sheet1',index_col=None,na_values=np.nan))
        del df['Unnamed: 0']
        del df['count']
        elem_ship = df['elem_ship'].values
        for i in range(len(elem_ship)):
            elem_ship[i] = elem_ship[i].replace('/','')
            elem_ship[i] = elem_ship[i].replace('\t','')
            elem_ship[i] = elem_ship[i].replace('\r','')
            elem_ship[i] = elem_ship[i].replace('\n','')
            elem_ship[i] = elem_ship[i].replace(' ','')
        df['elem_ship'] = elem_ship
        columns = df.columns
        for i in range(len(columns)):
            temp = df[columns[i]]
            temp = temp.dropna()
            if len(temp) == 0:
                del df[columns[i]]

        name = name.replace(',','')
        MD.create_table(name,df)
        MD.insert_data(name,df)
