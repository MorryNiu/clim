import socket
import threading
import sys

def build_server(host='0.0.0.0', port=8888):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket Created')
    except socket.error:
        print('Failed to create socket. Error code: {} , \
                Error message : '.format(str(msg[0]),str(msg[1])))
        sys.exit()

    sock.bind((host, port))

    sock.listen(10)
    print('Server', socket.gethostbyname(host), 'listening ...')

    while True:
        connection, addr = sock.accept()
        print('Accept a new connection', connection.getsockname(), connection.fileno())

        try:
            buf = connection.recv(1024).decode()
            if buf == '1':
                connection.send(b'welcome to server!')
                #open a new thread for current connection
                t = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
                t.setDaemon(True)
                t.start()
            else:
                connection.send(b'Too many people are there!')
                connection.close()
        except :
            pass

# send mes to all clients except exceptNum
def tellOthers(exceptNum, mes):
    for c in mylist:
        if c.fileno() != exceptNum :
            try:
                c.send(mes.encode())
            except:
                pass

def subThreadIn(myconnection, connNumber):
    nickname = myconnection.recv(1024).decode()
    mydict[myconnection.fileno()] = nickname
    mylist.append(myconnection)
    print('connection', connNumber, ' has nickname :', nickname)
    tellOthers(connNumber, '【PROMPT：'+mydict[connNumber]+'has entered the chat room】')

    while True:
        try:
            recvedMsg = myconnection.recv(1024).decode()
            if recvedMsg:
                print(mydict[connNumber], ':', recvedMsg)
                tellOthers(connNumber, mydict[connNumber]+' :'+recvedMsg)

        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            print(mydict[connNumber], 'exit, ', len(mylist), ' person left')
            tellOthers(connNumber, '【PROMPT：'+mydict[connNumber]+' has left the chat room 】')
            myconnection.close()
            return

mydict = {}
mylist = []

if __name__ == '__main__':
    build_server()
