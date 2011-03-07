# Copyright (c) 2011, Andy Ruse

# Setup of game objects and main game loop.

import os
import time
import optparse
import signal

import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from monster import *
from item import *
from dlevel import *
from cell import *
from ai import *
from gui import *
from spell import *
from keys import *
from actions import *


def monster_at(x, y):
    """Return the monster at location x, y."""
    for m in GC.monsters:
        if m.x == x and m.y ==y:
            return m

def load_game(file):
    f = open(file, 'r')
    exec(f.read())
    f.close()

    # Replace the map structure in the save file with actual cells.
    GC.map = map

    for x in range(len(GC.map)):
        for y in range(len(GC.map[0])):
            GC.map[x][y] = Cell(GC.map[x][y]['n'], explored=GC.map[x][y]['e'])

    # Replace oids with references to the actual objects.


def run_history():
    old_history = GC.cmd_history
    GC.cmd_history = []
    GC.state = ST_PLAYBACK

    for cmd in old_history:
        print 'Running ' + str(cmd)
        if cmd[0] == 'm':
            GC.u.move(cmd[1], cmd[2])
        elif cmd[0] == 'a':
            GC.u.attack(GC.obj_dict[cmd[1]])
        elif cmd[0] == 'p':
            GC.u.pick_up(GC.obj_dict[cmd[1]])
        elif cmd[0] == 'd':
            GC.u.drop(GC.obj_dict[cmd[1]])
        elif cmd[0] == 'u':
            GC.u.targeted_use(GC.obj_dict[cmd[1]], cmd[2], cmd[3])

        controller_tick()
        view_tick()

    GC.state = ST_PLAYING

def impossible(text):
    print 'Impossible area of code reached'
    print text
    exit
    
def handle_events():
    # Handle input events
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()
        elif event.type == KEYDOWN:
            GC.key = event
        elif event.type == KEYUP:
            GC.key = None
        elif event.type == MOUSEBUTTONDOWN:
            GC.button = event.button
        elif event.type == MOUSEBUTTONUP:
            GC.button = None
        elif event.type == MOUSEMOTION:
            pass
        elif event.type == VIDEORESIZE:
            handle_resize(event.w, event.h)

        # Handle scrolling
        GV.x_scrollbar.handle_event(event)
        GV.y_scrollbar.handle_event(event)
        GV.log_scrollbar.handle_event(event)

        handle_actions()


def monsters_take_turn():
    for m in GC.monsters:
        if m.ai:
            m.ai.take_turn()
        
def handle_actions():
    if GC.key:
        key_code, char, mod = GC.key.key, GC.key.unicode, GC.key.mod
        GC.key = None
    else:
        key_code, char, mod = None, None, None

    # Whether or not this keypress counts as taking a turn
    GC.u_took_turn = False
    
    if GC.state == ST_PLAYING:
        # Handle all keypresses
        if key_code:
            handled = False
            key_combo = ''

            if mod & KMOD_CTRL:
                key_combo = 'Ctrl + '

                if (key_code in GC.pkeys[KMOD_CTRL]
                    and GC.pkeys[KMOD_CTRL][key_code].action):
                    GC.pkeys[KMOD_CTRL][key_code].do()
                    handled = True

            elif mod & KMOD_ALT:
                key_combo = 'Alt + '

                if (key_code in GC.pkeys[KMOD_ALT]
                    and GC.pkeys[KMOD_ALT][key_code].action):
                    GC.pkeys[KMOD_ALT][key_code].do()
                    handled = True

            else:
                # First, look up by char.  If it's not found, then look up by
                # key_code.
                if (char in GC.pkeys[KMOD_NONE]
                    and GC.pkeys[KMOD_NONE][char].action):
                    GC.pkeys[KMOD_NONE][char].do()
                    handled = True
                elif (key_code in GC.pkeys[KMOD_NONE]
                    and GC.pkeys[KMOD_NONE][key_code].action):
                    GC.pkeys[KMOD_NONE][key_code].do()
                    handled = True

            if key_code not in ignore_keys and handled is False:
                if char in GC.pkeys[KMOD_NONE]:
                    key_to_print = char
                else:
                    key_to_print = pygame.key.name(key_code)
                message("Unknown command '{0}{1}'.".format(
                        key_combo, key_to_print))

    elif GC.state == ST_MENU:
        if key_code:
            if len(char) == 1:
                index = ord(char) - ord('a')
                if index >= 0 and index < len(GC.menu_options):
                    if GC.menu == 'use':
                        GC.state = ST_PLAYING # Exit menu
                        if len(GC.u.inventory) > 0:
                            item = GC.u.inventory[index]
                            if item is not None:
                                if GC.u.use(item) == 'success':
                                    GC.cmd_history.append(('u',
                                                           item.oid,
                                                           None, None))
                                    GC.u_took_turn = True
                                else:
                                    GC.u_took_turn = False
                                
                    elif GC.menu == 'drop':
                        GC.state = ST_PLAYING # Exit menu
                        GC.u_took_turn = True
                        if len(GC.u.inventory) > 0:
                            item = GC.u.inventory[index]
                            if item is not None:
                                GC.u.drop(item)
                else:
                    GC.state = ST_PLAYING # Exit menu
            else:        
                GC.state = ST_PLAYING # Exit menu

    elif GC.state == ST_TARGETING:
        if GC.button:
            x, y = pygame.mouse.get_pos()
            x, y = mouse_coords_to_map_coords(x, y)

            # Accept the target if the player clicked in FOV, and in
            # case a range is specified, if it's in that range
            if GC.button == BUTTON_L and GC.u.fov_map.in_fov(x, y):
                targeting_function = GC.targeting_function.pop(0)
                success = targeting_function(GC.targeting_item, x, y)

                # If this targeting is the result of an item use,
                # destroy the item
                if GC.targeting_item and success:
                    GC.cmd_history.append(('u', GC.targeting_item.oid, x, y))
                    GC.u.inventory.remove(GC.targeting_item)
                    GC.targeting_item = None
                    GC.u_took_turn = True
                    
            GC.state = ST_PLAYING
        elif key_code:
            message('Cancelled')
            GC.state = ST_PLAYING
    elif GC.state == ST_PLAYBACK:
        GC.u_took_turn = True
    elif GC.state == ST_QUIT:
        # Do nothing; let the main loop exit on its own.
        pass
    else:
        impossible('Unknown state: ' + GC.state)

    if GC.u_took_turn:
        GC.fov_recompute = True
        center_map()
        monsters_take_turn()
    else:
        GC.fov_recompute = False
        

def controller_tick(reel=False):
    """Handle all of the controller actions in the game loop."""

    if GC.state == ST_PLAYBACK:
        # Don't call clock.tick() in playback mode in order to make it
        # as fast as possible.
        handle_actions()
    else:
        GC.clock.tick(FRAME_RATE)
        GC.keys_handled = 0
        # Player takes turn
        handle_events()

    if GC.fov_recompute:
        GC.u.fov_map.do_fov(GC.u.x, GC.u.y, GC.u.fov_radius)
        GC.fov_recompute = False



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
    GC.clock = pygame.time.Clock()

       
    init_gv()
    GV.screen = pygame.display.set_mode(
        (GV.screen_rect.w, GV.screen_rect.h), pygame.RESIZABLE)

#    GV.log_surf = pygame.Surface((GV.log_rect.w, GV.log_rect.h)).convert()
    GV.eq_surf = pygame.Surface((GV.eq_rect.w, GV.eq_rect.h)).convert()
    GV.status_surf = pygame.Surface(
        (GV.status_rect.w, GV.status_rect.h)).convert()
    GV.map_surf = pygame.Surface((GV.map_rect.w, GV.map_rect.h)).convert()

    # Set the system icon
    system_icon = load_image('icon.xpm')
    pygame.display.set_icon(system_icon)
    
    GV.tiles_img = load_image('tiles16.xpm')
    GV.gray_tiles_img = load_image('tiles16_gray.xpm')
    GV.menu_bg_img = load_image('parchment.jpg')

    GV.tile_dict = create_tile_dict()
    GV.blank_tile = GV.tile_dict['cmap, wall, dark']


    if options.save_file:
        load_game(options.save_file)
        random.seed(GC.random_seed)
        GC.u = Player(0, 0, 'wizard')
    else:
        GC.u = Player(0, 0, 'wizard', fov_radius=10)
        GC.dlevel = 1
        GC.dlevel_dict['doom'] = []
        GC.dlevel_dict['doom'].append(gen_connected_rooms())
        GC.map = GC.dlevel_dict['doom'][0]
    
    # Create a dlevel
#    GC.map = gen_sparse_maze(MAP_W, MAP_H, 0.1)
#    GC.map = gen_perfect_maze(MAP_W, MAP_H)
    GC.u.set_fov_map(GC.map)
    


    # Have to call this once to before drawing the initial screen.
    GC.u.fov_map.do_fov(GC.u.x, GC.u.y, GC.u.fov_radius)
#    if options.save_file:
#        run_history()


    GV.x_scrollbar = ScrollBar(SCROLLBAR_W, 0, GV.map_rect,
                               GV.mapview_rect, always_show=False)
    GV.y_scrollbar = ScrollBar(SCROLLBAR_W, 1, GV.map_rect,
                               GV.mapview_rect, always_show=False)
    GV.log_scrollbar = ScrollBar(SCROLLBAR_W, 1, GV.log_rect,
                                 GV.logview_rect, always_show=False)

    # Make sure everything is aligned correctly
    center_map()
    handle_resize(GV.screen_rect.w, GV.screen_rect.h)

    attach_key_actions()

    message('Welcome, {0}!'.format(uname), GV.gold)
    message("""Moves the map surface so that the player appears at the center of the mapview.  If the map surface is smaller than the mapview, center the map inside of the mapview instead.""")

    # Main loop
    while GC.state != ST_QUIT:
        controller_tick()
        view_tick()
