# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Setup of game objects and main game loop.
"""

import os
import sys
import random
import time
import optparse

import pygame
from pygame.locals import *

from const import *
from common import *
from network import Network

from server.server_state import ServerState as SS
from server.server_main import *

from client.client_state import ClientState as CS
from client.client_cell import ClientCell
from client.client_monster import ClientMonster
from client.client_main import *
from client.client_map import ClientMap
    
def main():
    parser = optparse.OptionParser()
    parser.add_option('-s', '--input', dest='save_file', default='',
                      help='save_file FILE', metavar='FILE')
    (options, args) = parser.parse_args()

    init_server()
    init_client()

    # FIXME! - this should go in the response handler loop
    CS.map = ClientMap(SS.map.w, SS.map.h, SS.map.layout)
#    CS.map = [[ ClientCell('cmap, wall, dark') for y in xrange(MAP_H) ]
#           for x in xrange(MAP_W)]

    for x in xrange(MAP_W):
        for y in xrange(MAP_H):
            CS.map.grid[x][y].set_attr(SS.map.grid[x][y].name)

    from client.client_player import ClientPlayer
    CS.u = ClientPlayer(SS.u.x, SS.u.y, SS.u.name, SS.u.oid, fov_radius=10)
    CS.u.set_fov_map(CS.map.grid)
    CS.u.fov_map.do_fov(CS.u.x, CS.u.y, CS.u.fov_radius)
    attach_key_actions()

    # Make sure everything is aligned correctly
    center_map()
    handle_resize(CS.screen_rect.w, CS.screen_rect.h)

    # Main loop
    while CS.mode != ST_QUIT:
        server_tick()
        client_tick()
