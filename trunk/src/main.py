# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""Setup of game objects and main game loop."""

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
from client.client import Client as C
from util import *
from client.monster import *
from client.item import *
from server.dlevel import *
from client.cell import *
from server.ai import *
from client.gui import *
from server.spell import *
from client.keys import *
from server.requesthandler import *
from server.saveload import *
from stuff import *


def monster_at(x, y):
    """Return the monster at location x, y."""
    for m in S.monsters:
        if m.x == x and m.y ==y:
            return m

def run_history():
    old_history = S.cmd_history
    S.cmd_history = []
    S.state = ST_PLAYBACK

    for cmd in old_history:
        print 'Running ' + str(cmd)
        if cmd[0] == 'm':
            S.u.move(cmd[1], cmd[2])
        elif cmd[0] == 'a':
            S.u.attack(Object.obj_dict[cmd[1]])
        elif cmd[0] == ',':
            S.u.pick_up(Object.obj_dict[cmd[1]])
        elif cmd[0] == 'd':
            S.u.drop(Object.obj_dict[cmd[1]])
        elif cmd[0] == 'u':
            S.u.targeted_use(Object.obj_dict[cmd[1]], cmd[2], cmd[3])

        controller_tick()
        view_tick()

    S.state = ST_PLAYING

def impossible(text):
    print 'Impossible area of code reached'
    print text
    exit(0)
    
def handle_events():
    # Handle input events
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()
        elif event.type == KEYDOWN:
            S.key = event
        elif event.type == KEYUP:
            S.key = None
        elif event.type == MOUSEBUTTONDOWN:
            S.button = event.button
        elif event.type == MOUSEBUTTONUP:
            S.button = None
        elif event.type == MOUSEMOTION:
            pass
        elif event.type == VIDEORESIZE:
            handle_resize(event.w, event.h)

        # Handle scrolling
        C.x_scrollbar.handle_event(event)
        C.y_scrollbar.handle_event(event)
        C.log_scrollbar.handle_event(event)

        handle_actions()


def monsters_take_turn():
    for m in S.monsters:
        if m.ai:
            m.ai.take_turn()
        
def handle_actions():
    if S.key:
        key_code, char, mod = S.key.key, S.key.unicode, S.key.mod
        S.key = None
    else:
        key_code, char, mod = None, None, None

    # Whether or not this keypress counts as taking a turn
    S.u_took_turn = False
    
    if S.state == ST_PLAYING:
        # Handle all keypresses
        if key_code:
            handled = False
            key_combo = ''

            if mod & KMOD_SHIFT:
                if char not in S.pkeys[KMOD_NONE]:
                    key_combo = 'Shift + '

                if (key_code in S.pkeys[KMOD_SHIFT]
                    and S.pkeys[KMOD_SHIFT][key_code].action):
                    S.pkeys[KMOD_SHIFT][key_code].do()
                    handled = True

            elif mod & KMOD_CTRL:
                key_combo = 'Ctrl + '

                if (key_code in S.pkeys[KMOD_CTRL]
                    and S.pkeys[KMOD_CTRL][key_code].action):
                    S.pkeys[KMOD_CTRL][key_code].do()
                    handled = True

            elif mod & KMOD_ALT:
                key_combo = 'Alt + '

                if (key_code in S.pkeys[KMOD_ALT]
                    and S.pkeys[KMOD_ALT][key_code].action):
                    S.pkeys[KMOD_ALT][key_code].do()
                    handled = True

            if not handled:
                # First, look up by char.  If it's not found, then look up by
                # key_code.
                if (char in S.pkeys[KMOD_NONE]
                    and S.pkeys[KMOD_NONE][char].action):
                    S.pkeys[KMOD_NONE][char].do()
                    handled = True
                elif (key_code in S.pkeys[KMOD_NONE]
                    and S.pkeys[KMOD_NONE][key_code].action):
                    S.pkeys[KMOD_NONE][key_code].do()
                    handled = True

            if key_code not in ignore_keys and handled is False:
                if char in S.pkeys[KMOD_NONE]:
                    key_to_print = char
                else:
                    key_to_print = pygame.key.name(key_code)
                message("Unknown command '{0}{1}'.".format(
                        key_combo, key_to_print))

    elif S.state == ST_MENU:
        if key_code:
            if len(char) == 1:
                index = ord(char) - ord('a')
                if index >= 0 and index < len(S.menu_options):
                    if S.menu == 'use':
                        S.state = ST_PLAYING # Exit menu
                        if len(S.u.inventory) > 0:
                            item = S.u.inventory[index]
                            if item is not None:
                                request('a', (item.oid,))

#                                if S.u.use(item) == 'success':
#                                    S.cmd_history.append(('u',
#                                                           item.oid,
#                                                           None, None))
#                                    S.u_took_turn = True
#                                else:
#                                    S.u_took_turn = False
                                
                    elif S.menu == 'drop':
                        S.state = ST_PLAYING # Exit menu
                        S.u_took_turn = True
                        if len(S.u.inventory) > 0:
                            item = S.u.inventory[index]
                            if item is not None:
                                request('d', (item.oid,))
#                                S.u.drop(item)
                else:
                    S.state = ST_PLAYING # Exit menu
            else:        
                S.state = ST_PLAYING # Exit menu

    elif S.state == ST_TARGETING:
        if S.button:
            x, y = pygame.mouse.get_pos()
            x, y = mouse_coords_to_map_coords(x, y)

            # Accept the target if the player clicked in FOV, and in
            # case a range is specified, if it's in that range
            if S.button == BUTTON_L and S.u.fov_map.in_fov(x, y):
                targeting_function = S.targeting_function.pop(0)
                success = targeting_function(S.targeting_item, x, y)

                # If this targeting is the result of an item use,
                # destroy the item
                if S.targeting_item and success:
                    S.cmd_history.append(('u', S.targeting_item.oid, x, y))
                    S.u.inventory.remove(S.targeting_item)
                    del Object.obj_dict[S.targeting_item.oid]
                    S.targeting_item = None
                    S.u_took_turn = True
                    
            S.state = ST_PLAYING
        elif key_code:
            message('Cancelled')
            S.state = ST_PLAYING
    elif S.state == ST_PLAYBACK:
        S.u_took_turn = True
    elif S.state == ST_QUIT:
        # Do nothing; let the main loop exit on its own.
        pass
    else:
        impossible('Unknown state: ' + S.state)

    # Let the server side do its thing with the client requests we generated.
    handle_requests()


    if S.u_took_turn:
        S.fov_recompute = True
        center_map()
        monsters_take_turn()
    else:
        S.fov_recompute = False
        

def controller_tick(reel=False):
    """Handle all of the controller actions in the game loop."""

    if S.state == ST_PLAYBACK:
        # Don't call clock.tick() in playback mode in order to make it
        # as fast as possible.
        handle_actions()
    else:
        S.clock.tick(FRAME_RATE)
        S.keys_handled = 0
        # Player takes turn
        handle_events()

    if S.fov_recompute:
        S.u.fov_map.do_fov(S.u.x, S.u.y, S.u.fov_radius)
        S.fov_recompute = False



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
    S.clock = pygame.time.Clock()

       
    C.init_client()
    C.screen = pygame.display.set_mode(
        (C.screen_rect.w, C.screen_rect.h), pygame.RESIZABLE)

#    C.log_surf = pygame.Surface((C.log_rect.w, C.log_rect.h)).convert()
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

    
    S.map_rand = random.Random()
    S.rand = random.Random()

    if options.save_file:
        load_game(options.save_file)
        S.map_rand.seed(S.random_seed)
        S.rand.seed(S.random_seed)

    else:
        # We need to generate a random seed using the default-seeded random
        # number generator, and then save that to seed the game's generators.
        # This will allow us to easily use the same seed in order to duplicate
        # games.
        S.random_seed = str(random.randrange(sys.maxint))
        S.map_rand.seed(S.random_seed)
        S.rand.seed(S.random_seed)

        S.u = Player(0, 0, 'wizard', fov_radius=10)
        S.dlevel = 1
        S.dlevel_dict['doom'] = []
        S.dlevel_dict['doom'].append(gen_connected_rooms())
        S.map = S.dlevel_dict['doom'][0]
    

    S.u.set_fov_map(S.map)
    

    # Have to call this once to before drawing the initial screen.
    S.u.fov_map.do_fov(S.u.x, S.u.y, S.u.fov_radius)
#    if options.save_file:
#        run_history()


    C.x_scrollbar = ScrollBar(SCROLLBAR_W, 0, C.map_rect,
                               C.mapview_rect, always_show=False)
    C.y_scrollbar = ScrollBar(SCROLLBAR_W, 1, C.map_rect,
                               C.mapview_rect, always_show=False)
    C.log_scrollbar = ScrollBar(SCROLLBAR_W, 1, C.log_rect,
                                 C.logview_rect, always_show=False)

    # Make sure everything is aligned correctly
    center_map()
    handle_resize(C.screen_rect.w, C.screen_rect.h)

    attach_key_actions()
    attach_request_actions()

    message('Welcome, {0}!'.format(uname), S.gold)

    # Main loop
    while S.state != ST_QUIT:
        controller_tick()
        view_tick()
