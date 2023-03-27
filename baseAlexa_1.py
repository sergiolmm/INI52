import struct
import socket
import sys 
import _thread
import xml.etree.ElementTree as ET

import util as ut
import messages
from errno import ENOPROTOOPT


try:
    # Windows doesn't have SO_REUSEPORT
    from socket import SO_REUSEPORT
except ImportError:
    SO_REUSEPORT = None


def receive_multicast():
    group='239.255.255.250'
    mport=1900
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
    if SO_REUSEPORT is not None:
        sock.setsockopt(socket.SOL_SOCKET, SO_REUSEPORT, 1)     
    try:
        sock.bind(('0.0.0.0',mport))
        print('bind mcast\n')
    except socket.error:
        sock.bind(('', mport))
        #print('Listiong multicast on '+group+' port : '+ str(mport)+ '\n')
    #mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(group)+socket.inet_aton('0.0.0.0'))
    sock.settimeout(1)
      
    while True:
        try:
            (data, address) = sock.recvfrom(12000)
            #except socket.timeout:

                 #print (str(address) + ' >>\n' + data.decode() )
            if data:
                print (str(address) + ' >>\r\n' + data.decode() )
                msg = ut._read_headers(data.decode())
            
                if 'man' in msg.keys() or 'MAN' in msg.keys():
                    if '"ssdp:discover"' in msg.values():
                        sock.sendto(messages.resp.encode(), address)
                        print ('Enviado:\n'+str(address))

        except socket.timeout as ex:
            pass
        except Exception as ex:
            print(ex)
            continue
            

def on_new_client(clientesocket, addr):
    while True:
        msg = clientesocket.recv(1024)
        if msg:
            print (str(addr) + ' >>' + msg.decode() )
            break;

    print(str(addr))
    comando = ut._read_header_type(msg.decode())
    print(comando)
    request = ut._read_headers(msg.decode())
    print(request)
    
    



https = ut.get_ip()
hport = 8080

sockH = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sockH.bind((https,hport))
except socket.error:
    sockH.bind(('', hport))
except Exception:
    quit

sockH.listen(1)
print('Listiong HTTP on '+https+' port : '+ str(hport)+ '\n')

_thread.start_new_thread(receive_multicast,())

try:
    while True:
        c, addr = sockH.accept()
        _thread.start_new_thread(on_new_client,(c,addr))

except KeyboardInterrupt:
    print('Saindo')    
    
sockH.close()    