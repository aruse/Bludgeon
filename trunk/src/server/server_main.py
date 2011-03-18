# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

from server.server import Server as S

def handle_requests():
    """Handle requests coming in from the client."""
    while len(Network.client_requests):
        req, args = Network.client_requests.popleft()

        S.cmd_history.append((req, args))
        response = S.requests[req].do(args)
#        S.server_responses.append(response)


def server_init():
    """Initialize all of the server state."""
    pass

def server_main():
    """Main loop for the server."""
    handle_requests()
