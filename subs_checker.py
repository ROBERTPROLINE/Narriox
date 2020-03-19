import datetime
import time
import pymysql
import socket


db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','study_helper')
db_cur = db_conn.cursor()

db_cur.execute('Select * from users_cred')
print(db_cur.fetchall())

def main():
    pass
