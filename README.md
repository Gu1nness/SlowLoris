This is a simple implementation in Python3 of the Slow Loris attack.

=== What is Slow Loris ===

Slow Loris is a HTTP/HTTPs DoS attack that affects only threaded servers.
Basically,
the server open one new thread to answer the request it receives.
Then, the idea of Slow Loris is to open multiple connexions to the server and
to send the request very slowly.
Thus, the threads stay open, and if enough sockets are open, there is no thread
left to answer new requests.


=== To use it ===

Download the script by cloning the repo : ```git clone
https://github.com/Gu1nness/SlowLorris.git ```

Execute the following command : ```python3 slow_loris.py <address>

=== Get some help ===

The full list of options is here :
```
usage: slow_loris.py [-h] [-n NUMBER] [-p PORT] ADDRESS

Attacks the web server at the given IP with the Slow Loris attack

positional arguments:
  ADDRESS                The address or hostname to attack

  optional arguments:
    -h, --help            show this help message and exit
    -n NUMBER, --number NUMBER
                          Number of sockets to open (default=200)
    -p PORT, --port PORT  Port to attack
```
