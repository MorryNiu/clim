import socket
import time
import threading
import sys
from command import command as cd


def build_client(host='127.0.0.1', port=8888):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket Created')
    except socket.error:
        print('Failed to create socket. Error code: {} , \
                Error message : '.format(str(msg[0]),str(msg[1])))
        sys.exit()

    try:
        sock.connect((host, port))
        print('Connection built successfully')
    except:
        print('Connect failed.')
        sys.exit()

    sock.send(b'1')
    print(sock.recv(1024).decode())

    nickName = input('input your nickname: ')
    sock.send(nickName.encode())

    return sock


def sendThreadFunc(sock):
    global c_mode
    while True:
        try:
            word = input()
            if word == '$':
                c_mode = True
                cd(sock)
            else:
                sock.send(word.encode())
        except ConnectionAbortedError:
            print('Server closed this connection!')
        except ConnectionResetError:
            print('Server is closed!')


def recvThreadFunc(sock):
    global c_mode
    while True:
        try:
            otherword = sock.recv(1024)
            if otherword:
                print(otherword.decode())
                if c_mode:
                    print('-------------------command exit-----------------------')
                    c_mode = False
            else:
                pass
        except ConnectionAbortedError:
            print('Server closed this connection!')

        except ConnectionResetError:
            print('Server is closed!')


def main():
    sock = build_client()
    print('-------------------start chating-----------------------')
    th1 = threading.Thread(target=sendThreadFunc, args=(sock,))
    th2 = threading.Thread(target=recvThreadFunc, args=(sock,))
    threads = [th1, th2]
    for t in threads :
        t.setDaemon(True)
        t.start()
    t.join()

if __name__ == '__main__':
    c_mode = False
    main()
