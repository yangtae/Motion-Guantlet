# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

import pandas as pd
from bluetooth import *
import pyautogui as p
import keyboard
import sys

# Global Variable
w, h = p.size()
# p.PAUSE = 0
p.FAILSAFE = False

def connect_blutooth():
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service(server_sock, "SampleServer",
                      service_id=uuid,
                      service_classes=[uuid, SERIAL_PORT_CLASS],
                      profiles=[SERIAL_PORT_PROFILE],
                      protocols = [ OBEX_UUID ]
                      )

    print("Waiting for connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    return client_sock, client_info



if __name__ == "__main__":
    client_sock, client_info = connect_blutooth()
    df = pd.DataFrame()
    flag = False
    total = []
    
    try:
        while True:
            try: #used try so that if user pressed other than the given key error will not be shown
                
                if not keyboard.is_pressed('q'): continue
                
                count = 0
                datas = []
                
                while count < 20:
                    client_sock.send('ack')
                    recv = client_sock.recv(1024)
                    if len(recv) == 0: continue

                    data = recv.decode('ascii')
                    data = data.split()
                    datas = datas + data
                    count = count + 1
                
                total.append(datas)

                
            except:
                break #if user pressed a key other than the given key the loop will break
    except IOError:
        pass

    print("disconnected")
    df = pd.DataFrame(total)
    print(df.head())
    df.to_csv('right_2.csv')
    client_sock.close()
    print("all done")
