# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

from collections import deque

class Network:
    # Queue of requests coming from the client to the server.
    client_requests = deque()
    # Queue of responses from the server to the client.
    server_responses = deque()


def request(req, args):
    """Send a client request to the server.
    Arguments:
    req -- The request type, a string.
    args -- The arguments for the request, a tuple.
    """
    Network.client_requests.append((req, args))
    print 'Requests:', Network.client_requests
