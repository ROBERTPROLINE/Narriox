
import socket
import time
import sqlite3
import pymysql
import threading


class Client(threading.Thread):

    def __init__(self,threadID,name,soc):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name     = name
        self.soc      = soc



    def run(self):

        while 1:
            recvd = self.soc.recv(1024)
            if recvd.decode() == 'get_time':
                msg = str(time.ctime())
                self.soc.send(msg.encode('ascii'))
                time.sleep(20)


def main():
    counter = 0
    soc = socket.socket()
    port = 987
    ip = socket.gethostbyname(socket.gethostname())
    addr = (ip,port)
    soc.bind(addr)
    soc.listen(3)
    #print(addr)

    while True:
        client, addr = soc.accept()
        #print('new connection ->', addr)
        counter+=1
        nextThread = Client(counter, str(addr), client)
        nextThread.start()
main()
