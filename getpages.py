import socket
import sys


def getpages(host, port=80, new='new',print_header=False,create_file=False):

    """ input: str
        output: Null
        usage: get a web page,then print the head and save
               the contant as a html file
    """

    #create an TCP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket Created')
    except socket.error:
        print('Failed to create socket. Error code: {} , \
                Error message : '.format(str(msg[0]),str(msg[1])))
        sys.exit()

    try:
        s.connect((str(host), port))
        print('Connected')
    except:
        print('Cannot build a connection')
        sys.exit()

    # ask for the web page
    message = 'GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'.format(
        host
    )

    message = message.encode(encoding="utf-8")

    try:
        s.send(message)
    except socket.error:
        print('Send failed')
        sys.exit()

    print('Message send successfully')

    reply = []
    while True:
        d = s.recv(1024)
        if d:
            reply.append(d)
        else:
            break

    data = b''.join(reply)
    s.close()

    header, html = data.split(b'\r\n\r\n',1)

    if print_header:
        print(header.decode('utf-8'))

    if create_file:
        with open(new+'.html','wb') as f:
            f.write(html)

if __name__ == '__main__':
    getpages('www.baidu.com',create_file=True)
