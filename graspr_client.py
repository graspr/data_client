#!/usr/bin/python

import socket
import sys
from thread import start_new_thread
import numpy as np

sock = None

SOCK_HOST = 'graspr'
SOCK_PORT = 8081
SOCK_BACKLOG = 3

BUFFER_STEP = 1
BUFFERS = {
    1: np.zeros(120, 'f'),
    2: np.zeros(120, 'f'),
    3: np.zeros(120, 'f'),
    4: np.zeros(120, 'f'),
    5: np.zeros(120, 'f'),
    6: np.zeros(120, 'f'),
    7: np.zeros(120, 'f'),
    8: np.zeros(120, 'f'),
    9: np.zeros(120, 'f'),
    10: np.zeros(120, 'f'),
    11: np.zeros(120, 'f'),
    12: np.zeros(120, 'f'),
    13: np.zeros(120, 'f'),
    14: np.zeros(120, 'f'),
    15: np.zeros(120, 'f'),
    16: np.zeros(120, 'f'),
}

CURRENT_VAL = None

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
    print('Starting read Thread')
    start_new_thread(read_forever, ())

def read_forever():
    print('Reading values forever')
    while True:
        read()


def read():
    global sock, msg_raw, CURRENT_VAL
    msg_raw += sock.recv(4096)
    msg_len = len(msg_raw) 
    # .split(',') #get 16 values
    while msg_len < EXPECTED_MESSAGE_LENGTH:
        msg_raw += sock.recv(4096)

    msg_parts = msg_raw.split('\n')
    data = msg_parts[0]
    if len(msg_parts) > 1: #get msg_raw ready for next round
        msg_raw = ''.join(msg_parts[1:]) #keep the 'extra' bits around
    else:
        msg_raw = '' #start fresh

    data = data.split(',')
    data = map(lambda val: int(val,2), data)
    CURRENT_VAL = data
    update_buffers(CURRENT_VAL)
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

def update_buffers(data):
    for i in range(1,17):
        val = data[i-1]
        BUFFER = BUFFERS[i]
        BUFFER = np.roll(BUFFER, BUFFER_STEP)
        BUFFER[0] = val
        BUFFERS[i] = BUFFER

def get_buffer(probe_num):
    # print ('PNUM::%s' % probe_num)
    return BUFFERS[probe_num]


if __name__ == '__main__':
    setup_socket()
    while True:
        print get_buffer(15)
    