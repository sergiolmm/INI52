
lista = {}
lista['casa'] = 'valor'
lista['teste'] = 10
print(lista)

vetor = []
vetor.append(10)
vetor.append('casa')
print(vetor)

DISCOVER_TEMPLATE = b"""\
M-SEARCH * HTTP/1.1\r\n\
host: 239.255.255.250:1900\r\n\
man : "ssdp:discover"\r\n\
mx: 5\r\n\
st: upnp:rootdevice\r\n\
\r\n\
"""

print(DISCOVER_TEMPLATE)
dado = DISCOVER_TEMPLATE.decode()
print(dado)
header = dado.split('\r\n')
print('cabeçalho')
print(header)
cabecalho ={}
print('decomposto parcial' )
for linha in header[1:]:
    print(linha)
    dec_linha = linha.split(': ')
    chave = dec_linha[0]    
    if not chave == '':
       valor = dec_linha[1]
       cabecalho[chave] = valor

if 'upnp:rootdevice' in cabecalho.values():
    print(cabecalho)

# criar um procedimento que passado 
# string b' como parametro de entrada
# retorno uma lista(dict) caso encontre
# os valores de upnp:rootdevice ou
# ssdp:all
# caso não encotre retorno lista vazia.

# Apos conclusao iremos montar a resposta da
# solicitação do M-SEARCH.
# com o seguinte cabeçalho...
esp = b"""
HTTP/1.1 200 OK\r\n\
CACHE-CONTROL: max-age=86400\r\n\
DATE: Tue, 14 Dec 2016 02:30:00 GMT\r\n\
EXT:\r\n\
LOCATION: http://%(ip_addr)s:8080/setup.xml\r\n\
OPT: \"http://schemas.upnp.org/upnp/1/0/\"; ns=01\r\n\
01-NLS: %(uuid)s\r\n\
SERVER: Unspecified, UPnP/1.0, Unspecified\r\n\
X-User-Agent: redsonic\r\n\
ST: urn:Belkin:service:basicevent:1 \r\n\
USN: uuid:%(uuid)s::urn:Belkin:service:basicevent:1\r\n\
\r\n\
"""
ip_addr = get_ip() # será feita na aula que vem...
uuid = '38323636-4558-4dda-9188-cda0e6010703'
msg = esp % {b'uuid': uuid.encode('ascii')}
print(msg.decode())