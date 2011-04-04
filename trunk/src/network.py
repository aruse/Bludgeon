# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""Implement the Network class."""

from collections import deque


class Network(object):
    """
    Static class defining an interface to the network, either local
    or remote.
    """
    # Queue of requests coming from the client to the server.
    requests = deque()
    # Queue of responses from the server to the client.
    responses = deque()

    @classmethod
    def request(cls, req, args):
        """
        Send a client request to the server.
        Arguments:
        req -- The request type, a string.
        args -- The arguments for the request, a tuple.
        """
        Network.requests.append((req, args))
        print 'Requests:', Network.requests

    @classmethod
    def send_response(cls, res):
        """
        Send a response to the client.
        """
        Network.responses.append(res)
        print 'Responses:', Network.responses

    @classmethod
    def get_response(cls):
        """
        Return a complete server response.
        """
        if len(Network.responses):
            return Network.responses.popleft()
        else:
            return None
