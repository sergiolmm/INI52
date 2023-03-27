

import _thread
import threading
import time

# cria um evento de thread
event = threading.Event()

def teste_theard():    
    time.sleep(2.0)
    print("Oi..", end=' : ')
    print(time.strftime("%d-%m-%Y %X"))

def thread2(nome):
    while True:
        time.sleep(0.5)        
        print(nome + '... ' +time.strftime("%d-%m-%Y %X"))
        if event.is_set():
            print(nome + '. evento .. ' +time.strftime("%d-%m-%Y %X"))
            event.clear()
            break

def thread3():
    event.wait()
    print("Saindo do wait... "+time.strftime("%d-%m-%Y %X"))

print('Inicii : '+ time.strftime("%d-%m-%Y %X"))
_thread.start_new_thread(teste_theard,())
_thread.start_new_thread(thread3,())
_thread.start_new_thread(thread2,('PD rule´s',))

try:
    while True:
       time.sleep(3)
       event.set()
       time.sleep(10)
       print('Saindo : ' + time.strftime("%d-%m-%Y %X"))       
       quit()
except KeyboardInterrupt:
    print('Saindo')

