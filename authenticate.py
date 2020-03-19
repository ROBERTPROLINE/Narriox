import time
import threading
import socket
import random
import pymysql
import sqlite3
import datetime

exitFlag = 0






class Client(threading.Thread):

    


    class MessageService(threading.Thread):
        pass

    def __init__(self,threadID,addr,soc,db_conn,db_cur):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.addr     = addr
        self.soc      = soc
        self.online   = False
        self.db_conn = db_conn;
        self.db_cur = db_cur
        #self.ip_name = sqlite3.connect('data\\authentication\\auth.db')
        #self.cur2 = self.ip_name.cursor()
        

    def run(self):

        login = False
        subscr = False
        package = 'X'
        current_amt = 0


        crypt_code = 'crypt-{}'.format(str(random.random())[2:5])
        self.soc.send(crypt_code.encode('utf-8'))

        auth_req = self.soc.recv(208)
        
        user_cred = auth_req.decode().split('::')
        user_id = user_cred[0]
        #print(user_id)

        user_pwd = user_cred[-1]
       

        self.db_cur.execute("Select * from use_credentials where user_id = '{0}'".format(user_id))
        rzltz = self.db_cur.fetchone()
        
        if rzltz == None:
            self.soc.send('Authentication Failure '.encode('ascii'))
            self.soc.close()
            self.db_conn.close()
            return

        if user_pwd in rzltz:
            login = True
            
            #data should be removed after 20 minutes for re authentication
            #self.cur2.execute("insert into ip_name values('{}','{}')".format(self.addr,user_id))
            #self.ip_name.commit()

            self.db_cur.execute("select current_package, date_expiring from user_subs where user_id = '{}'".format(user_id))
            subs = self.db_cur.fetchone()
            #print(subs)
            package = subs[0]
            expir = subs[1]
            #print(package)
            #print(expir)

            day   = datetime.datetime.today().day
            month = datetime.datetime.today().month
            year  = datetime.datetime.today().year
            nw = '{}-{}-{}'.format(day,month,year)

            if(nw==expir):
                self.db_cur.execute("update user_subs set current_package = 'X' where user_id = '{}'".format(user_id))
                self.db_conn.commit()
                self.soc.send("package-expired".encode('ascii'))
                self.db_conn.close()
                return

            if package.upper() == 'X':
                self.soc.send("package-5".encode('ascii'))
                self.db_conn.close()
                return

            else:
                pcode = 'drman-{}'.format(package)
                self.soc.send(pcode.encode('ascii'))
                self.db_conn.close()
                return

        else:
            self.soc.send(str("Your subscription is illegal !!").encode('ascii')) 
            self.db_conn.close()   
        self.db_conn.close()
       

def main():
    counter = 0

    soc = socket.socket()
    port = 98
    ip = socket.gethostbyname(socket.gethostname())
    addr = (ip,port)
    soc.bind(addr)
    soc.listen(3)
    print(addr)

    while True:
        client, addr = soc.accept()

        db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','study_helper')
        db_cur = db_conn.cursor()
        nextThread = Client(counter, str(addr), client,db_conn,db_cur)
        nextThread.start()
try:
    main()
except Exception as ex:
    pass

    