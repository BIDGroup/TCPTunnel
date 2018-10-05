import socket
import sys
import time
import threading

def heartCheck(s):
    print "Heart Pack Thread Start"
    while True:
        try:
            data = s.recv(128)
            if not data:
                print "Heart Pack Tunnel Break"
                break
        except Exception:
            print "Heart Pack Tunnel Break"
            break

def link(s1,s2):
    while True:
        try:
            data = s1.recv(10240)
            if not data:
                s1.close();
                s2.close();
                break;
            s2.send(data)
        except Exception:
            s1.close()
            s2.close()
            break

print "### TCPTunnelClient ###"
print "Please Enter Local Server Port:"
localPort = int(raw_input())
localAddress = ('0.0.0.0', localPort)
print "Please Enter Re-Link Server Address:"
reLinkIP = raw_input()
print "Please Enter Re-Link Server Port:"
reLinkAddress = (reLinkIP, int(raw_input()))
print "Please Enter Remote Server Address:"
remoteIP = raw_input()
print "Please Enter Remote Server Port:"
remotePort = int(raw_input())
remoteAddress = (remoteIP, remotePort)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
s.bind(localAddress)
s.connect(remoteAddress)
s.send("Hello")
msg = s.recv(512)
print "Successful Link Remote Server!"
print "Get Link Address:", msg
s.close()
print "Start Local Server"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
s.bind(localAddress)
s.listen(localPort)
ss, addr = s.accept()
print "Heart Pack Tunnel Build"
t1 = threading.Thread(target = heartCheck, args=(ss,))
t1.setDaemon(True)
t1.start()
print "Start ReLink Service"
while True:
    client, addr = s.accept()
    print "Link From:", addr, "Start ReLink"
    reLinkClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    reLinkClient.connect(reLinkAddress)
    t2 = threading.Thread(target = link, args=(reLinkClient, client))
    t2.setDaemon(True)
    t2.start()
    t3 = threading.Thread(target = link, args=(client, reLinkClient))
    t3.setDaemon(True)
    t3.start()
