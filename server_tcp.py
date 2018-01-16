import socket
import threading
import sys
import time

def build_server(host='127.0.0.1',port=8888):

    #host = '127.0.0.1' # address of this computer itself
    #port = 8888 # arbitary non-privileged port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket Created')
    except socket.error:
        print('Failed to create socket. Error code: {} , \
                Error message : '.format(str(msg[0]),str(msg[1])))
        sys.exit()

    try:
        s.bind((host, port))
        print('Socket bind complete')
    except:
        print("Bind failed.")
        sys.exit()

    s.listen(10)
    print("Waiting for connections...")

    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()


def tcplink(sock, addr):
    print('Building a connection with {}:{}'.format(addr[0],addr[1]))
    sock.send(b'Welcome to the service')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Ok..{}'.format(data.decode('utf-8'))).encode(encoding='utf-8'))
    sock.close()
    print('Connection from {}:{} closed.'.format(addr[0],addr[1]))


if __name__ == '__main__':
    build_server()
