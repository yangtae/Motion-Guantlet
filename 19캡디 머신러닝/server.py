# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import pyautogui as p

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





def func(x, y, order):
    """
    :param order:
    :return :

    > function
    1 --> 커서 동작
    2 --> 방향키
    3 --> 커서 좌클릭
    4 --> 커서 우클릭
    """

    if order == '1':
        try:
            p.move(-x, -y)
        except ValueError:
            pass

    elif order == '2':
        pass
    elif order == '3':
        p.mouseDown(button='left')

    elif order == '4':
        p.mouseDown(button='right')

if __name__ == "__main__":
    client_sock, client_info = connect_blutooth()

    try:
        while True:
            data = client_sock.recv(512)
            if len(data) == 0: break
            # print("received [%s]" % data)
            data = data.decode('utf-8')
            data = data.split()
            # data[0]: x, data[1]: y, data[2]: order
            x = float(data[0])
            y = float(data[1])
            order = data[2]

            print(x, y, order)
            func(x,y,order)


    except IOError:
        pass

    print("disconnected")

    client_sock.close()
    server_sock.close()
    print("all done")
