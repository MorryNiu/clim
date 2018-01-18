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
        con, addr = sock.accept()
        print('Accept a new connection', con.getsockname(), con.fileno())

        try:
            buf = con.recv(1024).decode()
            if buf == '1':
                con.send(b'welcome to server!')
                #open a new thread for current connection
                t = threading.Thread(target=subThreadIn, args=(con, con.fileno()))
                t.setDaemon(True)
                t.start()
            else:
                con.send(b'Too many people are there!')
                con.close()
        except :
            pass

# send mes to all clients except exceptNum
def tellOthers(exceptNum, mes):
    for c in mylist:
        if c.fileno() != exceptNum :
            try:
                c.send(mes.encode())
            except:
                print('Failed to send message to '+str(mydict[c.fileno()]))


def tellOne(sock, mes):
    try:
        sock.send(mes.encode())
    except:
        print('Failed to send message to '+str(mydict[sock.fileno()]))


def command(con, conNum):
    print(mydict[conNum], 'is using command mode')
    clist = ['get_file','put_file','people']
    word = con.recv(1024).decode()
    if word == 'people':
        fre = []
        for p in mydict.values():
            fre.append(p)
        fre = list(set(fre))
        tellOne(con, ' '.join(fre))
    print('Finished ',mydict[conNum], '\'s work')


def subThreadIn(con, conNum):
    nickname = con.recv(1024).decode()
    mydict[con.fileno()] = nickname
    mylist.append(con)
    print('con', conNum, ' has nickname :', nickname)
    tellOthers(conNum, '【PROMPT：'+mydict[conNum]+' has entered the chat room】')

    while True:
        try:
            recvedMsg = con.recv(1024).decode()
            if recvedMsg:
                if recvedMsg == '$%$cm':
                    command(con, conNum)
                else:
                    print(mydict[conNum], ':', recvedMsg)
                    tellOthers(conNum, mydict[conNum]+' :'+recvedMsg)

        except (OSError, ConnectionResetError):
            try:
                mylist.remove(con)
            except:
                pass
            print(mydict[conNum], 'exit, ', len(mylist), ' person left')
            tellOthers(conNum, '【PROMPT：'+mydict[conNum]+' has left the chat room 】')
            con.close()
            return

mydict = {} # stroe the connection num:nickname
mylist = [] # stroe the connection (socket)

if __name__ == '__main__':
    build_server()
