
"""
Arquivo de mensagens para uso 

"""
import util as ut

message = 'projeto alexa python 1'

serial = '38323636-4558-4dda-9188-cda0e6010703'
 
persistent_uuid = 'Socket-1_0-' + serial

https = ut.get_ip()
hport = 8080


DISCOVER_TEMPLATE = b"""\
M-SEARCH * HTTP/1.1\r\n\
host: 239.255.255.250:1900\r\n\
man: "ssdp:discover"\r\n\
mx: 5\r\n\
st: %(st)s\r\n\
\r\n\
"""


resp = (
 'HTTP/1.1 200 OK\r\n'
 'CACHE-CONTROL: max-age=86400\r\n'
 'DATE: Tue, 14 Dec 2016 02:30:00 GMT\r\n'
 'EXT:\r\n'
 'LOCATION: http://' + ut.get_ip() + ':8080/setup.xml\r\n'
 'OPT: \"http://schemas.upnp.org/upnp/1/0/\"; ns=01\r\n'
 '01-NLS: '+persistent_uuid+'\r\n'
 'SERVER: Unspecified, UPnP/1.0, Unspecified\r\n'
 'X-User-Agent: redsonic'
 'ST: urn:Belkin:service:basicevent:1 \r\n'
 'USN: uuid:' + persistent_uuid + '::urn:Belkin:service:basicevent:1'#urn:Belkin:device:**' #upnp:rootdevice\r\n'
 '\r\n\r\n')

name = 'luz'


# Estado dispositivo 
#  Ligado True
#  Desligado False
estado_dispotivo = False 


setup_xml = (
    '<?xml version=\"1.0\"?>'
    '<root>'
    '<device>'
    '<deviceType>urn:Belkin:device:controllee:1</deviceType>'
    '<friendlyName>'+name+'</friendlyName>'
    '<manufacturer>Belkin International Inc.</manufacturer>'
    '<modelName>Emulated Socket</modelName>'
    '<modelNumber>3.1415</modelNumber>'
    '<UDN>uuid:'+persistent_uuid+'</UDN>'
    '<serviceList>'
      '<service>'
        '<serviceType>urn:Belkin:service:basicevent:1</serviceType>'
        '<serviceId>urn:Belkin:serviceId:basicevent1</serviceId>'
        '<controlURL>/upnp/control/basicevent1</controlURL>'
        '<eventSubURL>/upnp/event/basicevent1</eventSubURL>'
        '<SCPDURL>/eventservice.xml</SCPDURL>'
      '</service>'
      '<service>'
        '<serviceType>urn:Belkin:service:metainfo:1</serviceType>'
        '<serviceId>urn:Belkin:serviceId:metainfo1</serviceId>'
        '<controlURL>/upnp/control/metainfo1</controlURL>'
        '<eventSubURL>/upnp/event/metainfo1</eventSubURL>'
        '<SCPDURL>/metainfoservice.xml</SCPDURL>'
      '</service>'
    '</serviceList>'
  '</device>'
'</root>'
)



eventservice_xml = (
    '<scpd xmlns=\"urn:Belkin:service-1-0\">'
    '<specVersion><major>1</major><minor>0</minor></specVersion>'
    '<actionList>'
    '<action>'
    '<name>SetBinaryState</name>'
    '<argumentList>'
    '<argument>'
    '<retval />'
    '<name>BinaryState</name>'
    '<relatedStateVariable>BinaryState</relatedStateVariable>'
    '<direction>in</direction>'
    '</argument>'
    '</argumentList>'
    '</action>'
    '<action>'
    '<name>GetBinaryState</name>'
    '<argumentList>'
    '<argument>'
    '<retval/>'
    '<name>BinaryState</name>'
    '<relatedStateVariable>BinaryState</relatedStateVariable>'
    '<direction>out</direction>'
    '</argument>'
    '</argumentList>'
    '</action>'
    '</actionList>'
    '<serviceStateTable>'
    '<stateVariable sendEvents=\'yes\'>'
    '<name>BinaryState</name>'
    '<dataType>Boolean</dataType>'
    '<defaultValue>0</defaultValue>'
    '</stateVariable>'
    '<stateVariable sendEvents=\'yes\'>'
    '<name>level</name>'
    '<dataType>string</dataType>'
    '<defaultValue>0</defaultValue>'
    '</stateVariable>'
    '</serviceStateTable>'
    '</scpd>')


statusResponseTrue = (
    '<?xml version=\"1.0\" encoding=\"utf-8\"?>'
    '<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">'
    '<s:Body>'
    '<u:GetBinaryStateResponse xmlns:u=\"urn:Belkin:service:basicevent:1\">'
    '<BinaryState>1</BinaryState>'
    '</u:GetBinaryStateResponse>'
    '</s:Body>'
    '</s:Envelope>')

statusResponseFalse = (
    '<?xml version=\"1.0\" encoding=\"utf-8\"?>'
    '<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">'
    '<s:Body>'
    '<u:GetBinaryStateResponse xmlns:u=\"urn:Belkin:service:basicevent:1\">'
    '<BinaryState>0</BinaryState>'
    '</u:GetBinaryStateResponse>'
    '</s:Body>'
    '</s:Envelope>')


GET_TEMPLATE = b"""\
GET / HTTP/1.1\r\n\
host: 255.255.255.255:1900\r\n\
\r\n\
"""
GET_TEMPLATE1 = b"""\
GET /index.html HTTP/1.1\r\n\
host: 255.255.255.255:1900\r\n\
\r\n\
"""


if __name__ == '__main__':
    print(resp)
    print(setup_xml)
    print()
    print(ut.sendXML(setup_xml))

