# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Setup of game objects and main game loop.
"""

import optparse

import common.cfg as cfg
from server.server_main import server_init, server_tick
from client.client_state import ClientState as CS
from client.client_main import client_init, client_tick

def main():
    """
    Parse command line options, init client and server, and run the
    main game loop.
    """
    parser = optparse.OptionParser()
    parser.add_option('', '--id', dest='game_id', default='',
                      help='game_id ID', metavar='ID')
    (options, args) = parser.parse_args()

    server_init()
    client_init()

    # Main loop
    while CS.mode != cfg.ST_QUIT:
        server_tick()
        client_tick()
