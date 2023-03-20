import socket
import struct


SOCKET_TIMEOUT = 30  # ele é o dobro do delay existente no MX
SSDP_MULTICAST_ADDR = '239.255.255.250'
SSDP_MULTICAST_PORT = 1900
SSDP_MULTICAST_ADRR_PORT = (SSDP_MULTICAST_ADDR,SSDP_MULTICAST_PORT)

DISCOVER_TEMPLATE = b"""\
M-SEARCH * HTTP/1.1\r\n\
host: 239.255.255.250:1900\r\n\
man: "ssdp:discover"\r\n\
mx: 5\r\n\
st: %(st)s\r\n\
\r\n\
"""
st = 'upnp:rootdevice'
#st = 'ssdp:all'
# configurando o socket para poder fazer a conexão....

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
ttl_bin = struct.pack('@i', 2)
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2) #ttl_bin)
try:
    s.settimeout(SOCKET_TIMEOUT)
    msg = DISCOVER_TEMPLATE % {b'st': st.encode('ascii')}
    s.sendto(msg,SSDP_MULTICAST_ADRR_PORT)
    while True:
        res, addr = s.recvfrom(1024 + 512)
        resposta = res.decode()
        print("a",ends="")
        print(resposta)

except OSError:
    print("Deu o tempo, vamos decodificar")
    pass
finally:
    s.close()
