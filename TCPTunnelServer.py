import socket
import sys
import time
import threading

def heartCheck(s):
    print "Heart Pack Thread Start"
    while True:
        try:
            s.send(" ")
        except Exception:
            print "Head Check Tunnel Break"
            break

print "### TCPTunnelServer ###"
print 'Please Enter Listen Port:'
listenPort = int(raw_input())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
s.bind(('0.0.0.0',listenPort))
s.listen(200)
while True:
    print "Waiting For Connection"
    ss, remoteAddress = s.accept()
    print "Link From:", remoteAddress
    ss.send(remoteAddress.__str__())
    msg = ss.recv(512)
    print msg
    ss.close()
    time.sleep(2)
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s1.connect(remoteAddress)
    print "Heart Pack Tunnel Build"
    t1 = threading.Thread(target = heartCheck, args=(s1,))
    t1.setDaemon(True)
    t1.start()
