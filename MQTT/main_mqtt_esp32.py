print("Hello, ESP32 MQTT EXAMPLE  !")


import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
import onewire, ds18x20
from machine import Pin #  biblioteca machine

help(onewire)

ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
 
roms = ds_sensor.scan()
print('Found DS devices: ', roms)
 

ds_sensor.convert_temp()
time.sleep_ms(750)
for rom in roms:
  print(rom)
  print(ds_sensor.read_temp(rom))



print("Connecting to WiFi", end="")
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect('Wokwi-GUEST', '')
while not station.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")


led = Pin(27, Pin.OUT)

mqtt_server = 'test.mosquitto.org'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'hello'

last_message = 0
message_interval = 1 #5. tempo de leitura em segundos. 
counter = 0

print('Connection successful')
print(station.ifconfig())

  

def read_ds_sensor():
  roms = ds_sensor.scan()
 # print('Found DS devices: ', roms)
 # print('Temperatures: ')
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  for rom in roms:
    temp = ds_sensor.read_temp(rom)
    if isinstance(temp, float):
      msg = round(temp, 2)
  #    print(temp, end=' ')
  #    print('Valid temperature')
      return msg
  return b'0.0'

temp = read_ds_sensor()
#print(temp)

# Complete project details at https://RandomNerdTutorials.com

def sub_cb(topic, msg):
  print((topic, msg))
  # aqui verifica a mensaem enviada
  if topic == b'notification' and msg == b'on':
    led.value(1)
  if topic == b'notification' and msg == b'off':  
    led.value(0)
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      temp = read_ds_sensor()
      msg = b'Hello #%d temp: %d' %(counter,temp)
      print('publicando... ', msg, ' -> ',topic_pub)  
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()