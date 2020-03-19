import pymysql
import socket
import threading
import datetime
import sqlite3
import socket

#get account details from local socket




class NewUser(threading.Thread):

   
    def __init__(self,conn,addr,db_conn,db_cur):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.db_conn = db_conn;
        self.db_cur = db_cur

    def run(self):
         #check fro duplicate entry before processing account
        data = self.conn.recv(2048)
        

        dy = datetime.datetime.today().day
        mnth  = datetime.datetime.today().month
        yr = datetime.datetime.today().year

        today_ = '{}-{}-{}'.format(dy,mnth,yr)

        user_details = data.decode()
        user_datails = user_details.split(',')
        uid = user_datails[0]
        pwd =  user_datails[1]    
        fstname = user_datails[2]
        lstname = user_datails[3]
        email = user_datails[4]
        phone = user_datails[5]
        exp_ = user_datails[6]
        #print(user_datails)
        #print(type(user_datails))
        self.db_cur.execute("select * from use_credentials where user_id = '{}'".format(uid));
        rzltz = self.db_cur.fetchone()
        if rzltz == None:
            course_table = uid + '_courses'
                                                        #userid-fname-lname-dob-sch-degree-lvl :: user_personal
                                                        #userid-password-email-phone :: use_credentials
                                                        #userid-toatlapaid-amt-package-susdate : user_subs
                                                        #userid-lvl-coursetable : user_prefs
            self.db_cur.execute("insert into use_credentials values('{}','{}','{}','{}')".format(uid,pwd,email,phone))
            self.db_cur.execute("insert into user_personal values('{}','{}','{}','{}','{}','{}','{}')".format(uid,fstname,lstname,'birthdae','school','program','lvl'))
            self.db_cur.execute("insert into user_subs values('{}','{}','{}','{}','{}','{}')".format(uid,'0','0','trial',today_,exp_))
            #Register courses after confirmation of phone , email and that customer is student
		    #self.db_cur.execute("insert into user_prefs values('{}','{}','{}')".format(uid,lvl,course_table))
              

        self.db_conn.commit()
            self.conn.send('create-account-success'.encode('ascii'))
            self.db_conn.close()
        else:
            self.conn.send('Please choose another username'.encode('ascii')
            self.db_conn.close()    
       
        self.db_conn.close()



def CreateAccount():

    soc = socket.socket()
    ip = socket.gethostbyname(socket.gethostname())
    port = 912
    addr = ((ip,port))
    soc.bind(addr)
    soc.listen(2)

    #print(addr)

    while True:
        conn ,addr = soc.accept()
        db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','study_helper')
        db_cur = db_conn.cursor()
        newconn = NewUser(conn, addr,db_conn,db_cur)
        newconn.start()
            
                


CreateAccount()        