DISCOVER_TEMPLATE = b"""\
M-SEARCH * HTTP/1.1\r\n\
host: 239.255.255.250:1900\r\n\
man: "ssdp:discover"\r\n\
mx: 5\r\n\
st: %(st)s\r\n\
\r\n\
"""

esp = b"""
HTTP/1.1 200 OK\r\n\
CACHE-CONTROL: max-age=86400\r\n\
DATE: Tue, 14 Dec 2016 02:30:00 GMT\r\n\
EXT:\r\n\
LOCATION: http://' + get_ip() + ':8080/setup.xml\r\n\
OPT: \"http://schemas.upnp.org/upnp/1/0/\"; ns=01\r\n\
01-NLS: %(uuid)s\r\n\
SERVER: Unspecified, UPnP/1.0, Unspecified\r\n\
X-User-Agent: redsonic\r\n\
ST: urn:Belkin:service:basicevent:1 \r\n\
USN: uuid:%(uuid)s::urn:Belkin:service:basicevent:1\r\n\
\r\n\
"""
uuid = '38323636-4558-4dda-9188-cda0e6010703'
msg = esp % {b'uuid': uuid.encode('ascii')}
print(msg.decode())