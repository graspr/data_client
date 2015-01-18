#!/usr/bin/python

import socket
import sys
from thread import start_new_thread
import numpy as np
import time
import deal_with_args

sock = None

SOCK_HOST = 'graspr'
SOCK_PORT = 8087
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

EXPECTED_MESSAGE_LENGTH = 95 #expect 16vals * 16 bits + 15commas +\n = 272
msg_raw = ''

def setup_socket(PORT=None, fake_data=False):
    if fake_data:
        return start_new_thread(read_forever, (True,))

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

def read_forever(fake_data=False):
    print('Reading values forever')

    #Seperate while loops so we don't check the if statement every time.
    if fake_data:
        read_fake() #this has a for loop inside of it.
    else:
        while True:
            read()

def read_fake():
    # print 'DOING FAKE DATA'
    NUM_VALUES = 100
    data = np.linspace(0, 2*np.pi, num=NUM_VALUES)
    data = np.sin(data)
    data *= (65535/2)
    data += (65535/2)
    data = map(lambda val: int(val), data)
    i = 0;
    while True:
        if i>= NUM_VALUES:
            i = 1 #1 instead of 0 to take out the kink
        update = [data[i] for x in range(1,17)]
        # print 'THIS IS THE UPDATE: %s' % update
        update_buffers(update)
        i = i + 1
        time.sleep(0.02) #~60 fps

def read():
    global sock, msg_raw, CURRENT_VAL
    msg_raw += sock.recv(EXPECTED_MESSAGE_LENGTH)

    msg_len = len(msg_raw) 
    while msg_len < EXPECTED_MESSAGE_LENGTH:
        recv = sock.recv(120)
        msg_raw += recv
        msg_len += len(recv)

    msg_parts = msg_raw.split('\n')
    data = msg_parts[0]
    if len(msg_parts) > 1: #get msg_raw ready for next round
        msg_raw = ''.join(msg_parts[1:]) #keep the 'extra' bits around
    else:
        msg_raw = '' #start fresh

    data = data.split(',')
    # print 'PRE_PROCESSED DATA: %s' % data
    data = map(lambda val: int(val), data)
    update_buffers(data)
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
    global CURRENT_VAL
    CURRENT_VAL = data
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
    input_args = deal_with_args.get_results()
    setup_socket(PORT=input_args.port[0], fake_data=input_args.fake_data)
    while True:
        print get_buffer(15)
    