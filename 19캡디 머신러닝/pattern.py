from bluetooth import *
import pyautogui as p
import pickle
from time import sleep

# Global Variable
w, h = p.size()
# p.PAUSE = 0
p.FAILSAFE = False

global loaded_model
global X


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


def find_pattern(data):
    global X
    global loaded_model
    
    if len(data) == 7:
        if len(X) == 140:
            X = X[7:]

        X = X + data
        if len(X) == 140:
                pred = loaded_model.predict([X])
                if pred == 1:
                    print('find pattern')
                else:
                    print('Not find..')

        
    


if __name__ == "__main__":
    X = []
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    client_sock, client_info = connect_blutooth()

    try:
        while True:
            client_sock.send('send')
            recv = client_sock.recv(4096)
            data = recv.decode('ascii')
            data = data.split()
            find_pattern(data)
            sleep(0.003)
            
        
    except IOError:
        pass

    print("disconnected")

    client_sock.close()
    print("all done")
