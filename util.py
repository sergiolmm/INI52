import socket
import re

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def _read_header_type(response):
    if type(response) == bytes:
        return _read_header_type_sb(response)
    headers = {}
    lines = response.split('\r\n')
    # line 0 is HTTP/1.1
    header_lines = lines[0:1]
    for line in header_lines:
        if len(line) > 0:
            m = re.match(r'(\S+?) (.*) HTTP(.*)', line)
            if m:
                key = m.group(1).upper()
                headers[key] = m.group(2)
    return headers

def _read_header_type_sb(response):
    assert type(response) == bytes
    lines = response.split(b'\r\n')
    return {
        k.decode(): (''.join(map(chr, v))).split(' ',1)[0] for [k, v] in (line.split(b' ', 1) for line in lines[:1] if b'/' in line)
    }


def _read_headers(response):
    if type(response) == bytes:
        return _read_headersb(response)
    headers = {}
    lines = response.split('\r\n')
    # line 0 is HTTP/1.1
    header_lines = lines[1:]
    for line in header_lines:
        if len(line) > 0:
            m = re.match(r'(\S+?): (.*)', line)
            if m:
                key = m.group(1).upper()
                headers[key] = m.group(2)
    return headers

def _get_ip_port(response):
    ip_p = ()
    lines = response.split(':')    
    return (lines[0], int(lines[1]))
    


def _read_headersb(response):
    assert type(response) == bytes
    lines = response.split(b'\r\n')
    return {
        k.decode(): ''.join(map(chr, v)) for [k, v] in (line.split(b': ', 1) for line in lines[1:] if b': ' in line)
    }


def sendXML(msg):
   resp = ('HTTP/1.1 200 OK\r\n'
           'Content-Type: text/xml\r\n'
           'Connection: close\r\n'  
           '\r\n' + msg + '\r\n\r\n')
   return resp 

def sendHTTP(msg):
   resp = ('HTTP/1.1 200 OK\r\n'
           'Content-Type: text/html\r\n'
           'Connection: close\r\n'  
           '\r\n' + msg + '\r\n\r\n')
   return resp 


if __name__ == '__main__':
    ip = '255.255.255.255:65555'
    print(_get_ip_port(ip))

    import messages as msg

    print(_read_header_type(msg.GET_TEMPLATE1))
    print(_read_header_type(msg.GET_TEMPLATE1.decode()))

    print('Testando get_ip() -> ', end='')
    print(get_ip())

    assert True  # levanta ou não um erro de assert no python que pode ser tratado ou não

   



    st = 'ssdp:all'
    template1 = msg.DISCOVER_TEMPLATE % {b'st': st.encode('ascii')}
    msg = _read_headersb(template1)
    print(msg)
    msg = _read_headers(template1.decode())
    print(msg)

    print('desmontando')
    lines = template1.split(b'\r\n')
    # for line in lines[1:] if b': ' in line)
    parte1 = lines[1:]
    parte2 = []
    print(parte1)
    for line in parte1:
        if b': ' in line:
            parte2.append(line)
    print(parte2)
    parte3 = {}
    for dado in parte2:
        #line.split(b': ', 1)
        k,v = dado.split(b': ', 1)
        print(k,v)
        #DECODIFICA CHAVE
        k1 = k.decode()
        print(k1)
        #DECODIFICA VALOR
        v1 = ''.join(map(chr, v))
        print(v1)
        # CRIA DICIONARIO
        parte3[k1]=v1
    print(parte3)        
    #return {
    #    k.decode(): ''.join(map(chr, v)) for [k, v] in (line.split(b': ', 1) for line in lines[1:] if b': ' in line)


