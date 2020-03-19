import time
import socket

def main():
    s = socket.socket()
    ip = '127.0.0.1'
    port = 0
    addr = (ip,port)
    s.bind(addr)
    saddr = (('127.0.0.1',987))
    s.connect(saddr)


    while 1:

        s.send('get_time'.encode('ascii'))

        data = s.recv(1024)
        print(data.decode())
main()
