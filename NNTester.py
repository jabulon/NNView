import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 9000))
clientsocket.send(b'warning -an desktop 1 40 16 192.168.220.40 1935 live stream1')
clientsocket.close()

def drop():
    return()