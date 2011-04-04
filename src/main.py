# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Setup of game objects and main game loop.
"""

import optparse

from const import *
from common import *

from server.server_state import ServerState as SS
from server.server_main import server_init, server_tick

from client.client_state import ClientState as CS
from client.client_monster import ClientMonster
from client.client_main import client_init, client_tick
from client.client_map import ClientMap
from client.keys import *
import client.gui as gui

def main():
    """
    Parse command line options, init client and server, and run the
    main game loop.
    """
    parser = optparse.OptionParser()
    parser.add_option('-s', '--input', dest='save_file', default='',
                      help='save_file FILE', metavar='FILE')
    (options, args) = parser.parse_args()

    server_init()
    client_init()

    # Make sure everything is aligned correctly
    gui.center_map()
    gui.handle_resize(CS.screen_rect.w, CS.screen_rect.h)

    # Main loop
    while CS.mode != ST_QUIT:
        server_tick()
        client_tick()
