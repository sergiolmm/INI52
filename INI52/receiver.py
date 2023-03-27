# RECEIVER
import socket
import struct
import utils
MCAST_GRP = '239.255.255.250'
MCAST_PORT = 1900


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
while True:
    dado_bruto, addr = sock.recvfrom(10240)
    dado = dado_bruto.decode()
    print(utils._read_header2(dado))

    #st = 'upnp:rootdevice'
    #st = 'ssdp:all'
    if dado.__contains__('upnp:rootdevice'):
        print(dado)
        #header = dado.split('\r\n')
        #print('cabeçalho')
        #print(header)
        #print('decomposto parcial' )
        #for linha in header[1:]:
        #    print(linha)
        #header2 = {}
        
