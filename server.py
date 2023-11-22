import socket as sck
import AlphaBot
import time
from threading import Thread
import sqlite3

SEPARATOR = ';'
SEPARATOR_DB = '-'

# creazione socket tcp server
s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
# creazione istanza AlphaBot
r = AlphaBot.AlphaBot()

conDb = sqlite3.connect("./TabMovements.db")
curDb = conDb.cursor()

class ThreadLed(Thread):
    def __init__(self, connesione):
        super().__init__()
        self.connessione = connesione

    def run(self):
        while True:
            self.connessione.sendall(f'{r.getSensoLeft()}{SEPARATOR}{r.getSensoRight()}'.encode())
            # SB: print(f'{r.getSensoLeft()}{SEPARATOR}{r.getSensoRight()}'.encode())
            time.sleep(1)


def playMov(command, duration):
    if command.lower() == 'b':
        r.backward()
        time.sleep(duration)
        r.stop()
    elif command.lower() == 'f':
        r.forward()
        time.sleep(duration)
        r.stop()
    elif command.lower() == 'r':
        r.right()
        time.sleep(duration)
        r.stop()
    elif command.lower() == 'l':
        r.left()
        time.sleep(duration)
        r.stop()
    else:
        cDb(command)

def cDb(command):
    q = f"SELECT MovSequence FROM TABLE_MOVEMENTS WHERE Shortcut = '{command.lower()}'"

    movSeq = curDb.execute(q)

    ms = movSeq.fetchall()
    if(len(ms) == 0):
        playMov('f', 0)
    else:
        cList = str(ms[0][0]).split(SEPARATOR_DB)
        
        for mov in cList:
            playMov(mov.split(SEPARATOR)[0], float(mov.split(SEPARATOR)[1]))

def main():
    # bind
    address = ('0.0.0.0', 5000)
    s.bind(address)
    s.listen()
    
    while True:
        connesione, clientAddress = s.accept()
        thread = ThreadLed(connesione)
        thread.start()
        mex = connesione.recv(4096).decode() # mex decodificato in ascii

        # mex command example: f;10
        splitMex = mex.split(SEPARATOR)

        if len(splitMex) != 2:
            print('error')
            continue # continua il ciclo senza eseguire l'istruzione rimanente

        command = splitMex[0]
        duration = int(splitMex[1])

        if command.lower() == 'e':
            break
        # duration in second
        playMov(command, duration)

    conDb.close()
    connesione.close()
    s.close()


if __name__ == '__main__':
    main()
