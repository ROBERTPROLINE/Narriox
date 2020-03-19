#request to subscribe from client

import socket
import time
import sqlite3
import pymysql
import threading
import winsound
import datetime



class Client(threading.Thread):

    def __init__(self,threadID,addr,soc,db_conn,db_cur):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.addr    = addr
        self.soc      = soc
        self.db_conn = db_conn;
        self.db_cur = db_cur
      

    def run(self):

        subscr = False
        package_amt = 0
        package = 'X'
        current_amt = 0
        self.soc.send('subs-approv'.encode('ascii'))

        data = self.soc.recv(1048)
        dec_data = data.decode()
        print(dec_data)

        subs_req = dec_data.split('::')
        user_id = subs_req[0]
        user_pwd = subs_req[1]
        package = subs_req[2]
       
        self.db_cur.execute("select * from use_credentials where user_id = '{0}'".format(user_id))
        udata = self.db_cur.fetchone()
        print('Processing user ', user_id, 'with package : ', package)

        if udata[1]==user_pwd:

            self.db_cur.execute("Select * from packages where package_name = '{0}'".format(package))
            pkdata = self.db_cur.fetchone()
            package_amt = int(pkdata[-1])
            print('package amt = : ', package_amt)

            self.db_cur.execute("Select * from user_subs where user_id = '{0}'".format(user_id))
            subs_data = self.db_cur.fetchone()

            current_amt = int(subs_data[-4]) 
            print('Current user amt : ', current_amt)

            if current_amt>= package_amt:
                new_bal = current_amt - package_amt
                subscr = True
                self.db_cur.execute("update user_subs set amt = '{0}' where user_id = '{1}'".format(new_bal,user_id))
                self.db_cur.execute("update user_subs set current_package = '{0}' where user_id = '{1}'".format(package,user_id))
                ##
                day   = datetime.datetime.today().day
                month = datetime.datetime.today().month
                year  = datetime.datetime.today().year
                ##
                self.db_cur.execute("update user_subs set date_subscribed = '{0}-{1}-{2}' where user_id = '{3}'".format(day,month,year,user_id))

                self.db_conn.commit()
                self.soc.send('msg-notify -> Subscription Complete : '.encode('ascii'))
                print('Subscription Complete ')
                self.db_conn.close()
                
            else:
                self.soc.send('msg-notify -> Insufficient Funds to process transaction'.encode('ascii'))
                #print('insufficeint funds')
                self.db_conn.close()
        else:
            self.soc.send('msg-notify -> Failed : Common Error'.encode('ascii'))
            self.db_conn.close()

        #self.db_conn.close()    
        
      
            
def main():
    counter = 0

    soc = socket.socket()
    port = 9812
    ip = socket.gethostbyname(socket.gethostname())
    addr = (ip,port)
    soc.bind(addr)
    soc.listen(3)
    print(addr)

    while True:
        client, addr = soc.accept()
        print('new connection from ', addr)
        
        db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','study_helper')
        db_cur = db_conn.cursor()
        nextThread = Client(counter, addr, client,db_conn,db_cur)
        nextThread.start();
try:
    main()
except Exception as ex:
    pass    
    