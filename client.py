# CORREZIONE PROF
import socket as sck
from threading import Thread

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

LED_TRUE = '0'
LED_FALSE = '1'

SEPARATOR = ';'
SERVER_ALPHABOT = ('192.168.1.144',5000)

def sendCommands():
    command = input('inserire un comando: ')
    duration = input('inserire durata: ')
    mex = f'{command}{SEPARATOR}{duration}'.encode()

    # invio mex
    s.sendall(mex)

    if command.lower() == 'e':
        s.close()

class ThreadLed(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            sensor = s.recv(4096).decode().split(SEPARATOR)

            if len(sensor) == 2:

                if sensor[0] == LED_TRUE and sensor[1] == LED_TRUE:
                    print("ostacolo DAVANTI")
                    sendCommands()

                elif sensor[0] == LED_TRUE and sensor[1] == LED_FALSE:
                    print("ostacolo SINISTRA")
                    sendCommands()

                elif sensor[1] == LED_TRUE and sensor[0] == LED_FALSE:
                    print("ostacolo DESTRA")
                    sendCommands()

                elif sensor[0] == LED_FALSE and sensor[1] == LED_FALSE:
                    print("ostacolo NONE")
                    sendCommands()

def main():
    s.connect(SERVER_ALPHABOT)
    t = ThreadLed()
    t.start()

if __name__ == '__main__':
    main()