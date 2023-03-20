import socket
import struct

SOCKET_TIMEOUT = 30  # ele é o dobro do delay existente no MX
SSDP_MULTICAST_ADDR = '239.255.255.250'
SSDP_MULTICAST_PORT = 1900
SSDP_MULTICAST_ADRR_PORT = (SSDP_MULTICAST_ADDR,SSDP_MULTICAST_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('',SSDP_MULTICAST_PORT))
mrep = struct.pack("4sl", socket.inet_aton(SSDP_MULTICAST_ADDR), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mrep)
while True:
    res =  sock.recv(10240)
    print(res)
