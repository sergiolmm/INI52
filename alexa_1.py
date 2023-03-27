import socket
import _thread

import util as ut
import messages as msg1
import messages

from errno import ENOPROTOOPT

# para uso da rede em ambinte não windows
try:
    from socket import SO_REUSEPORT
except ImportError:
    SO_REUSEPORT = None

def receive_multicast():
    group = '239.255.255.250'
    mport = 1900
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
    if SO_REUSEPORT is not None:
        sock.setsockopt(socket.SOL_SOCKET, SO_REUSEPORT, 1)
    try:
        sock.bind(('0.0.0.0', mport))
        print('bind mcast')
    except socket.error:
        sock.bind(('', mport))

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(group)+ socket.inet_aton('0.0.0.0'))        
    sock.settimeout(1)
    #  recebendo dados
    while True:
        try:
            (data, address) = sock.recvfrom(12000)            
            #print(str(address) + ' >>\n' +  data.decode())
            if data:
                hearder = ut._read_headers(data.decode())
                if 'man' in hearder.keys() or 'MAN' in hearder.keys():
                    if '"ssdp:discover"' in hearder.values():
                        sock.sendto(messages.resp.encode(), address)
                        print(str(address)+ "->> Respondendo a solicitaçao")

        except socket.timeout as ex:
            pass
        except Exception as ex1:
            print(ex1)
            continue            


def on_new_client(sock, addr):
    while True:
        msg = sock.recv(1024)
        if msg:
            print(str(addr) + ' >>\n' + msg.decode())
            
            msgRet = ut.sendHTTP("Alo turma")
            sock.send(msgRet.encode())
            


_thread.start_new_thread(receive_multicast,())

# criar um servidor http na port 8080
https = ut.get_ip()
hport = 8080

sockH = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sockH.bind((https, hport))
except socket.error:
    sockH.bind(('', hport))
except Exception:
    quit()

sockH.listen(10)
print("Escutando em "+ https + ' na porta '+ str(hport))

try:
    while True:
        client_sock, addr = sockH.accept()
        _thread.start_new_thread(on_new_client,(client_sock, addr))

except KeyboardInterrupt:
    print('Saindo')        

sockH.close()