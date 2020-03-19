#complete payment made by ecocash with approvalcode
#only works with ecocash payments - Ecocash zimbabwe mobile money platform

import threading
import socket
import time
import datetime
import pymysql
import sqlite3
import random

exitFlag = 0



class Client:

    def __init__(self,soc,addr,db_conn,db_cur):
        threading.Thread.__init__(self)
        self.soc = soc
        self.addr =addr
        self.db_conn = db_conn;
        self.db_cur = db_cur

    def run(self):
        
        claim = self.soc.recv(2048)
        claim_data = claim.decode('ascii')

        claim_details = claim_data.split('::')
        #print(claim_data)
        uid = claim_details[0]
        amt = claim_details[1]
        approvalCode = claim_details[2]
        payee = claim_details[3]
        amt = 0

        self.db_cur.execute("select * from use_credentials where user_id = '{}'".format(uid))
        ret = self.db_cur.fetchone()

        if ret == None:
            self.soc.send("Account Not Found".encode('ascii'))
            self.db_conn.close()
            pass
            

        self.db_cur.execute("select * from payments where approvalCode = '{}'".format(approvalCode))
        retval = self.db_cur.fetchone()
        #amt varchar(45), approvalCode varchar(45), payee varchar(45), claim_status varchar(45), claimer varchar(45)
        if retval == None:
            self.soc.send("Funds associated with aprroval code not found!!".encode('ascii'))
            self.db_conn.close()
            pass
            
        elif retval[3] == "not-claimed":
           if retval[1] == approvalCode:
               self.db_cur.execute("update payments set claim_status = 'claimed' where approvalCode = '{}'".format(approvalCode))
               self.db_cur.execute("update payments set claimer = '{}' where approvalCode = '{}'".format(uid,approvalCode))
               self.db_conn.commit()
               

               #update user amt in user_subs
               self.db_cur.execute("select totalpaid, amt from user_subs where user_id = '{}'".format(uid))
               mnz = self.db_cur.fetchone()
               #print('m',mnz)

               totalpaid = int(mnz[0]) + int(retval[0])
               amt = int(mnz[1]) + int(retval[0])

               self.db_cur.execute("update user_subs set totalpaid = '{}' where user_id = '{}'".format(totalpaid,uid))
               self.db_cur.execute("update user_subs set amt = '{}' where  user_id = '{}'".format(amt,uid))
               self.db_conn.commit();
               self.db_conn.close()
               self.soc.send("Payment Done !!".encode('ascii'))
               self.db_conn.close()
               pass
        elif retval[3] == "claimed":
            self.soc.send("Funds already claimed !\nIf funds beloned to you Please\nLodge a complaint now!!".encode('ascii'))
            self.db_conn.close()
            pass
            

        else:
           self.soc.send("Claim error !\nCheck details you supplied!".encode('ascii')) 
           self.db_conn.close()
           pass
        #self.db_conn.close()

def main():
    
    
    soc = socket.socket()
    ip = socket.gethostbyname(socket.gethostname())
    port = 9009
    addr = ((ip,port))
    soc.bind(addr)
    soc.listen(2)

    #print(addr)

    while True:
        
        conn ,addr_ = soc.accept()
        #print(addr_)
        db_conn = pymysql.connect('localhost','pythonroot422913','claire6772147','study_helper')
        db_cur = db_conn.cursor()
        newconn = Client(conn, addr,db_conn,db_cur)
        newconn.run()
            
                
try:
    main()
except Exception as ex:
    pass





































