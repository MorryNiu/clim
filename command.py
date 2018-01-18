import os
import socket

def command(sock):
    print('-------------------command mode-----------------------')
    clist = ['help','exit','get_file','put_file','people']
    while True:
        c = str(input('>> '))
        c = c.lower()
        if c in clist:
            if c == 'help':
                print(clist[1:])
            elif c == 'exit' :
                exit()
                return
            elif c == 'get_file':
                sock.send(b'$%$cm')
            elif c == 'put_file':
                add = input('Please enter the file address: ')
                sock.send(b'$%$cm')
            elif c == 'people':
                sock.send(b'$%$cm')
                sock.send(b'people')
                return
        else:
            print('Command not found, use EXIT to exit command mode')

def feedback(sock):
    buf = ''
    while True:
        data = sock.recv(1024)
        if data:
            buf += data
        else:
            print('pass')
            return buf

def exit():
    print('-------------------command exit-----------------------')
