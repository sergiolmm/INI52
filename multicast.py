import struct
import socket
import sys 
import _thread
import xml.etree.ElementTree as ET

import util as ut
from errno import ENOPROTOOPT


group='239.255.255.250'
mport=1900

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP = ut.get_ip()
try:
    sock.bind((IP,mport))
    print('bind mcast\n')
except socket.error:
    sock.bind(('', mport))
        #print('Listiong multicast on '+group+' port : '+ str(mport)+ '\n')
      #mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(group) + socket.inet_aton(IP))
sock.settimeout(1)
      
while True:
    try:
        data, address = sock.recvfrom(12000)
            #except socket.timeout:
    except:
        continue
            
            #print (str(address) + ' >>\n' + data.decode() )
    if data:
        print(data)
        msg = data.decode()
        print(msg)

 