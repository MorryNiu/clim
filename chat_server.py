import socket
import threading
import sys

def build_server(host='127.0.0.1', port=8888):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket Created')
    except socket.error:
        print('Failed to create socket. Error code: {} , \
                Error message : '.format(str(msg[0]),str(msg[1])))
        sys.exit()

    try:
        sock.bind((host, port))
        print('Socket bind to {}:{} complete'.format(host,port))
    except:
        print("Bind failed.")
        sys.exit()

    sock.listen(5)
    print('Server', socket.gethostbyname('localhost'), 'listening ...')

    while True:
        connection, addr = sock.accept()
        print('Accept a new connection', connection.getsockname(), connection.fileno())
        try:
            #connection.settimeout(5)
            buf = connection.recv(1024).decode()
            if buf == '1':
                connection.send(b'welcome to server!')

                #为当前连接开辟一个新的线程
                mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
                mythread.setDaemon(True)
                mythread.start()

            else:
                connection.send(b'Too many people are there!')
                connection.close()
        except :
            pass

#把whatToSay传给除了exceptNum的所有人
def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum :
            try:
                c.send(whatToSay.encode())
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
