import sqlite3
import os
class MyDB():
    conn=None
    cursor=None
    def __init__(self,path):
        self.conn = sqlite3.connect(path)
        self.cursor=self.conn.cursor()

    def sql(self,sql_command):
        print(sql_command)
        cursor=self.cursor.execute(sql_command)
        self.conn.commit()
        
        return cursor

    def select(self,table,what,condition=""):
        if condition!="":
            condition=" WHERE {condition}".format(condition=condition)
        sql="SELECT {what} from {table}".format(what=what,table=table)+condition
        return self.sql(sql)
        
    def insert(self,table,keys,values):
        sql="INSERT INTO {table} ({keys}) \
            VALUES {values}".format(keys=keys,table=table,values=values)
        self.sql(sql)
        self.conn.commit()


if __name__ == "__main__":
    mydb=MyDB("fuck.db")
    mydb.insert("md5,Quote",("a","b"),"fuvk")
    

