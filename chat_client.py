import socket
import time
import threading
import sys


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
    while True:
        try:
            word = input()
            if word == '$':
                command(sock)
            else:
                sock.send(word.encode())
        except ConnectionAbortedError:
            print('Server closed this connection!')
        except ConnectionResetError:
            print('Server is closed!')


def recvThreadFunc(sock):
    while True:
        try:
            otherword = sock.recv(1024)
            if otherword:
                print(otherword.decode())
            else:
                pass
        except ConnectionAbortedError:
            print('Server closed this connection!')

        except ConnectionResetError:
            print('Server is closed!')


def command(sock):
    print('-------------------command mode-----------------------')
    clist = ['exit','get_file']
    while True:
        c = str(input('>> '))
        c = c.lower()
        if c in clist:
            if clist.index(c) == 0:
                print('-------------------command exit-----------------------')
                return
        else:
            print('Command not found, use EXIT to exit command mode')


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
    main()
