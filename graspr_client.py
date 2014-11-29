#!/usr/bin/python

import socket
import sys

sock = None

SOCK_HOST = 'graspr'
SOCK_PORT = 8081
SOCK_BACKLOG = 3

EXPECTED_MESSAGE_LENGTH = 272 #expect 16vals * 16 bits + 15commas +\n = 272
msg_raw = ''

def setup_socket(PORT=None):
    global sock
    # Create a TCP/IP socket
    try:
        print('Creating socket...'),
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()
    print('Created.')
    # Bind the socket to the port
    server_address = (SOCK_HOST, PORT or SOCK_PORT)
    print('starting up on {} port {}'.format(*server_address))
    try:
        print('Attempting to bind socket...'),
        sock.connect(server_address)
        print('Bound!')
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    print('Successful bind.')

def read():
    global sock, msg_raw
    msg_raw += sock.recv(4096)
    msg_len = len(msg_raw) 
    # .split(',') #get 16 values
    while msg_len < EXPECTED_MESSAGE_LENGTH:
        msg_raw += sock.recv(4096)

    msg_parts = msg_raw.split('\n')
    data = msg_parts[0].split(',')
    if len(msg_parts) > 1: #get msg_raw ready for next round
        msg_raw = ''.join(msg_parts[1:]) #keep the 'extra' bits around
    else:
        msg_raw = '' #start fresh

    data = map(lambda val: int(val,2), data)
    return data

def moving_average(iterable, n=3):
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    # http://en.wikipedia.org/wiki/Moving_average
    it = iter(iterable)
    d = deque(itertools.islice(it, n-1))
    d.appendleft(0)
    s = sum(d)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / float(n)


if __name__ == '__main__':
    setup_socket()
    while True:
        read()
    