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
import signal

import pygame
from pygame.locals import *

from const import *
from server.server import Server as S
from server.cell import *
from server.monster import *
from server.item import *
from server.dlevel import *
from server.ai import *
from server.requesthandler import *
from server.saveload import *
from server.spell import *
from server.server_main import *

from client.client import Client as C
from client.client_cell import *
from client.client_monster import *
from client.client_item import *
from client.gui import *
from client.keys import *

from network import Network
from util import *
from stuff import *


    
def handle_events():
    # Handle input events
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()
        elif event.type == KEYDOWN:
            C.key = event
        elif event.type == KEYUP:
            C.key = None
        elif event.type == MOUSEBUTTONDOWN:
            C.button = event.button
        elif event.type == MOUSEBUTTONUP:
            C.button = None
        elif event.type == MOUSEMOTION:
            pass
        elif event.type == VIDEORESIZE:
            handle_resize(event.w, event.h)

        # Handle scrolling
        C.x_scrollbar.handle_event(event)
        C.y_scrollbar.handle_event(event)
        C.log_scrollbar.handle_event(event)

    if C.key:
        key_code, char, mod = C.key.key, C.key.unicode, C.key.mod
        C.key = None
    else:
        key_code, char, mod = None, None, None

    if C.state == ST_PLAYING:
        # Handle all keypresses
        if key_code:
            handled = False
            key_combo = ''

            if mod & KMOD_SHIFT:
                if char not in C.pkeys[KMOD_NONE]:
                    key_combo = 'Shift + '

                if (key_code in C.pkeys[KMOD_SHIFT]
                    and C.pkeys[KMOD_SHIFT][key_code].action):
                    C.pkeys[KMOD_SHIFT][key_code].do()
                    handled = True

            elif mod & KMOD_CTRL:
                key_combo = 'Ctrl + '

                if (key_code in C.pkeys[KMOD_CTRL]
                    and C.pkeys[KMOD_CTRL][key_code].action):
                    C.pkeys[KMOD_CTRL][key_code].do()
                    handled = True

            elif mod & KMOD_ALT:
                key_combo = 'Alt + '

                if (key_code in C.pkeys[KMOD_ALT]
                    and C.pkeys[KMOD_ALT][key_code].action):
                    C.pkeys[KMOD_ALT][key_code].do()
                    handled = True

            if not handled:
                # First, look up by char.  If it's not found, then look up by
                # key_code.
                if (char in C.pkeys[KMOD_NONE]
                    and C.pkeys[KMOD_NONE][char].action):
                    C.pkeys[KMOD_NONE][char].do()
                    handled = True
                elif (key_code in C.pkeys[KMOD_NONE]
                    and C.pkeys[KMOD_NONE][key_code].action):
                    C.pkeys[KMOD_NONE][key_code].do()
                    handled = True

            if key_code not in ignore_keys and handled is False:
                if char in C.pkeys[KMOD_NONE]:
                    key_to_print = char
                else:
                    key_to_print = pygame.key.name(key_code)
                message("Unknown command '{0}{1}'.".format(
                        key_combo, key_to_print))

    elif C.state == ST_MENU:
        if key_code:
            if len(char) == 1:
                index = ord(char) - ord('a')
                if index >= 0 and index < len(C.menu_options):
                    if C.menu == 'use':
                        C.state = ST_PLAYING # Exit menu
                        if len(C.u.inventory) > 0:
                            item = C.u.inventory[index]
                            if item is not None:
                                Network.request('a', (item.oid,))

                    elif C.menu == 'drop':
                        C.state = ST_PLAYING # Exit menu
                        if len(C.u.inventory) > 0:
                            item = C.u.inventory[index]
                            if item is not None:
                                Network.request('d', (item.oid,))
                else:
                    C.state = ST_PLAYING # Exit menu
            else:        
                C.state = ST_PLAYING # Exit menu

    elif C.state == ST_TARGETING:
        if C.button:
            x, y = pygame.mouse.get_pos()
            x, y = mouse_coords_to_map_coords(x, y)

            # Accept the target if the player clicked in FOV, and in
            # case a range is specified, if it's in that range
            if C.button == BUTTON_L and C.u.fov_map.in_fov(x, y):
                targeting_function = C.targeting_function.pop(0)
                success = targeting_function(C.targeting_item, x, y)

                # If this targeting is the result of an item use,
                # destroy the item
                if C.targeting_item and success:
                    C.cmd_history.append(('u', C.targeting_item.oid, x, y))
                    C.u.inventory.remove(C.targeting_item)
                    del Object.obj_dict[C.targeting_item.oid]
                    C.targeting_item = None
                    
            C.state = ST_PLAYING
        elif key_code:
            message('Cancelled')
            C.state = ST_PLAYING
    elif C.state == ST_PLAYBACK:
        pass
    elif C.state == ST_QUIT:
        # Do nothing; let the main loop exit on its own.
        pass
    else:
        impossible('Unknown state: ' + C.state)

    # Let the server side do its thing with the client requests we generated.
    handle_requests()


def client_tick(reel=False):
    """
    Handle server responses, player input, and updating the client gui.
    """

    # If there are any server responses, handle them.
    res = Network.get_response()
    while res:

        # Update log messages
        if 'log' in res:
            for msg in res['log']:
                C.msgs.append(msg)

            C.log_updated = True

        # Update monsters
        if 'm' in res:
            for oid, m_str in res['m'].iteritems():
                if oid in ClientObject.obj_dict:
                    ClientObject.obj_dict[oid].update_from_string(m_str)
                else:
                    m = ClientMonster.unserialize(m_str)
                    C.monsters.append(m)
                    C.map[m.x][m.y].monsters.append(m)

        # Update items
        if 'i' in res:
            for oid, i_str in res['i'].iteritems():
                if oid in ClientObject.obj_dict:
                    ClientObject.obj_dict[oid].update_from_string(i_str)
                else:
                    i = ClientItem.unserialize(i_str)
                    C.items.append(i)
                    C.map[i.x][i.y].items.append(i)

        # Update the player object
        if 'u' in res:
            C.u.update_from_string(res['u'])
            C.u.fov_map.do_fov(C.u.x, C.u.y, C.u.fov_radius)
            center_map()
            

        res = Network.get_response()



    if C.state != ST_PLAYBACK:
        C.clock.tick(FRAME_RATE)
        # Player takes turn
        handle_events()

    update_gui()



def main():
    # Set up signal handlers
    signal.signal(signal.SIGINT, quit_game)
    signal.signal(signal.SIGTERM, quit_game)

    # Initializing these modules separately instead of calling
    # pygame.init() is WAY faster.
    pygame.display.init()
    pygame.font.init()

    # Wait 200 ms before repeating a key that's held down, and send them
    # as fast as possible.  The repeat delay is therefore limited by the
    # frame rate, not by set_repeat()
    pygame.key.set_repeat(200, 1)

    pygame.display.set_caption('{0} {1}'.format(GAME_NAME, VERSION))

    parser = optparse.OptionParser()
    parser.add_option('-s', '--input', dest='save_file', default='',
                      help='save_file FILE', metavar='FILE')
    (options, args) = parser.parse_args()


    uname = 'Taimor'
    usex = 'Male'
    urace = 'Human'
    urole = 'Wizard'
    
    pygame.display.set_caption('{0} - {1} the {2} {3} {4}'.format(
            GAME_TITLE, uname, usex, urace, urole))

    
    # Prepare game objects
    C.clock = pygame.time.Clock()

       
    C.init_client()
    C.screen = pygame.display.set_mode(
        (C.screen_rect.w, C.screen_rect.h), pygame.RESIZABLE)
    C.eq_surf = pygame.Surface((
        C.eq_rect.w, C.eq_rect.h)).convert()
    C.status_surf = pygame.Surface((
        C.status_rect.w, C.status_rect.h)).convert()
    C.map_surf = pygame.Surface((
        C.map_rect.w, C.map_rect.h)).convert()

    # Set the system icon
    system_icon = load_image('icon.xpm')
    pygame.display.set_icon(system_icon)
    
    C.tiles_img = load_image('tiles16.xpm')
    C.gray_tiles_img = load_image('tiles16_gray.xpm')
    C.menu_bg_img = load_image('parchment.jpg')

    C.tile_dict = create_tile_dict()
    C.blank_tile = C.tile_dict['cmap, wall, dark']
    
    C.x_scrollbar = ScrollBar(SCROLLBAR_W, 0, C.map_rect,
                               C.mapview_rect, always_show=False)
    C.y_scrollbar = ScrollBar(SCROLLBAR_W, 1, C.map_rect,
                               C.mapview_rect, always_show=False)
    C.log_scrollbar = ScrollBar(SCROLLBAR_W, 1, C.log_rect,
                                 C.logview_rect, always_show=False)

    init_server()


    # FIX! - this should go in the response handler loop
    C.map = [[ ClientCell('cmap, wall, dark') for y in range(MAP_H) ]
           for x in range(MAP_W)]

    for x in range(MAP_W):
        for y in range(MAP_H):
            C.map[x][y].set_attr(S.map[x][y].name)

    C.u = ClientPlayer(S.u.x, S.u.y, S.u.name, S.u.oid, fov_radius=10)
    C.u.set_fov_map(C.map)
    C.u.fov_map.do_fov(C.u.x, C.u.y, C.u.fov_radius)
    attach_key_actions()


    # Make sure everything is aligned correctly
    center_map()
    handle_resize(C.screen_rect.w, C.screen_rect.h)


    # Main loop
    while C.state != ST_QUIT:
        server_tick()
        client_tick()
