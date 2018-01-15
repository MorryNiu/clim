import socket
import sys

def client(host='127.0.0.1',port=8888):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket Created')
    except socket.error:
        print('Failed to create socket. Error code: {} , \
                Error message : '.format(str(msg[0]),str(msg[1])))
        sys.exit()

    try:
        s.connect((host, port))
        print("Connected successfully")
    except:
        print("Cannot built a connection")

    print(s.recv(1024).decode('utf-8'))

    for data in [b'Morry',b'James']:
        s.send(data)
        print(s.recv(1024).decode('utf-8'))

    s.send(b'exit')

    s.close()

if __name__ == '__main__':
    client()
