#!/usr/bin/env python

# Copyright (c) 2011, Andy Ruse

import os
import time
import optparse

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

import pickle

def save_game(file):
    f = open(file, 'w')
    pickle.dump(GC.dlevel, f)
    pickle.dump(GC.branch, f)
    pickle.dump(GC.msgs, f)
    pickle.dump(GC.oid_seq, f)
#    pickle.dump(GC.obj_dict, f)
    pickle.dump(GC.random_seed, f)
    pickle.dump(GC.random_state, f)
    pickle.dump(GC.cmd_history, f)
    pickle.dump(GC.dlevel_dict, f)
#    pickle.dump(GC.u, f)
#    pickle.dump(GC.monsters_dict, f)
#    pickle.dump(GC.items_dict, f)
    f.close()
#    f = open(file, 'w')
#    f.write('GC.random_seed = {0}\n'.format(GC.random_seed))
#    f.write('GC.cmd_history = {0}\n'.format(GC.cmd_history))
#    for var in dir(GC):
#        print 'GC.{0} = {1}'.format(var, eval('GC.' + var))


def monster_at(x, y):
    """Return the monster at location x, y."""
    for m in GC.monsters:
        if m.x == x and m.y ==y:
            return m

def load_game(file):
    f = open(file, 'r')
    pickle.load(f)
#    exec(f.read())
    f.close()

def run_history():
    old_history = GC.cmd_history
    GC.cmd_history = []
    GC.state = 'playback'

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

    GC.state = 'playing'

def impossible(text):
    print 'Impossible area of code reached'
    print text
    exit
    
def handle_events():
    # Handle input events
    for event in pygame.event.get():
        if event.type == QUIT:
            GC.state = 'exit'
        elif event.type == KEYDOWN:
            GC.prev_key = GC.key
            GC.key = event.key
        elif event.type == KEYUP:
            GC.prev_key = GC.key
            GC.key = None
        elif event.type == MOUSEBUTTONDOWN:
            GC.button = event.button
        elif event.type == MOUSEBUTTONUP:
            GC.button = None

        handle_actions()


def monsters_take_turn():
    for m in GC.monsters:
        if m.ai:
            m.ai.take_turn()
        
def handle_actions():
    # If an action has already been taken this clock cycle, don't do another one.
    if GC.action_handled and GC.state != 'playback':
        return

    # Whether or not this keypress counts as taking a turn
    u_took_turn = False
        
    if GC.state == 'playing':
        # Exit the game
        if GC.key == K_ESCAPE:
            GC.state = 'exit'
        elif GC.key == K_UP or GC.key == K_KP8:
            GC.u.try_move(DIRH['u'])
            u_took_turn = True
        elif GC.key == K_DOWN or GC.key == K_KP2:
            GC.u.try_move(DIRH['d'])
            u_took_turn = True
        elif GC.key == K_LEFT or GC.key == K_KP4:
            GC.u.try_move(DIRH['l'])
            u_took_turn = True
        elif GC.key == K_RIGHT or GC.key == K_KP6:
            GC.u.try_move(DIRH['r'])
            u_took_turn = True
        elif GC.key == K_KP7:
            GC.u.try_move(DIRH['ul'])
            u_took_turn = True
        elif GC.key == K_KP9:
            GC.u.try_move(DIRH['ur'])
            u_took_turn = True
        elif GC.key == K_KP1:
            GC.u.try_move(DIRH['dl'])
            u_took_turn = True
        elif GC.key == K_KP3:
            GC.u.try_move(DIRH['dr'])
            u_took_turn = True
        elif GC.key:
            char = pygame.key.name(GC.key)

            if char == 's':
                save_file = 'save.bludgeon'
                save_game(save_file)
                message('Saved game to {0}.'.format(save_file))
            elif char == '.':
                GC.cmd_history.append(('m', 0, 0))
                u_took_turn = True
            elif char == ',':
                item_here = False
                for i in GC.items:
                    if i.x == GC.u.x and i.y == GC.u.y:
                        GC.u.pick_up(i)
                        item_here = True

                if item_here:
                    u_took_turn = True
                else:
                    message('Nothing to pick up!')

            elif char == 'i':
                inventory_menu('Press the key next to an item to use it, or any other to cancel.')
                GC.menu = 'use'

            elif char == 'd':
                inventory_menu('Press the key next to an item to drop it, or any other to cancel.')
                GC.menu = 'drop'

            else:
                message(pygame.key.name(GC.key) + ' pressed')

    elif GC.state == 'menu':
        if GC.key:
            char = pygame.key.name(GC.key)

            if len(char) == 1:
                index = ord(char) - ord('a')
                if index >= 0 and index < len(GC.menu_options):
                    if GC.menu == 'use':
                        GC.state = 'playing' # Exit menu
                        if len(GC.u.inventory) > 0:
                            item = GC.u.inventory[index]
                            if item is not None:
                                if GC.u.use(item) == 'success':
                                    GC.cmd_history.append(('u', item.oid, None, None))
                                    u_took_turn = True
                                else:
                                    u_took_turn = False
                                
                    elif GC.menu == 'drop':
                        GC.state = 'playing' # Exit menu
                        u_took_turn = True
                        if len(GC.u.inventory) > 0:
                            item = GC.u.inventory[index]
                            if item is not None:
                                GC.u.drop(item)
                else:
                    GC.state = 'playing' # Exit menu
            else:        
                GC.state = 'playing' # Exit menu

    elif GC.state == 'targeting':
        if GC.button:
            x, y = pygame.mouse.get_pos()
            x, y = mouse_coords_to_map_coords(x, y)

            # Accept the target if the player clicked in FOV, and in case a range is specified, if it's in that range
            if GC.button == BUTTON_L and GC.u.fov_map.lit(x, y):
                targeting_function = GC.targeting_function.pop(0)
                success = targeting_function(GC.targeting_item, x, y)

                # If this targeting is the result of an item use, destroy the item
                if GC.targeting_item and success:
                    GC.cmd_history.append(('u', GC.targeting_item.oid, x, y))
                    GC.u.inventory.remove(GC.targeting_item)
                    GC.targeting_item = None
                    u_took_turn = True
                    
            GC.state = 'playing'
        elif GC.key:
            message('Cancelled')
            GC.state = 'playing'
    elif GC.state == 'playback':
        u_took_turn = True
    elif GC.state == 'exit':
        pass
    else:
        impossible('Unknown state: ' + GC.state)

    if u_took_turn:
        GC.fov_recompute = True
        monsters_take_turn()
    else:
        GC.fov_recompute = False
        
    GC.action_handled = True
        

def controller_tick(reel=False):
    """Handle all of the controller actions in the game loop."""

    if GC.state == 'playback':
        # Don't call clock.tick() in playback mode in order to make it as fast as possible.
        handle_actions()
    else:
        GC.clock.tick(FRAME_RATE)
        GC.action_handled = False
        
        # Player takes turn
        handle_events()

        if GC.key == GC.prev_key:
            GC.key_held += 1
        else:
            GC.key_held = 0
            
        # If a key has been held down long enough, repeat the action
        if GC.key_held > REPEAT_DELAY:
            handle_actions()

        GC.prev_key = GC.key

    if GC.fov_recompute:
        GC.u.fov_map.do_fov(GC.u.x, GC.u.y, 10)
        GC.fov_recompute = False



def main():
    # Initializing these modules separately instead of calling pygame.init() is WAY faster.
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption('{0} {1}'.format(GAME_NAME, VERSION))

    parser = optparse.OptionParser()
    parser.add_option("-s", "--input", dest="save_file", default='',
                      help="save_file FILE", metavar="FILE")
    (options, args) = parser.parse_args()

    if options.save_file:
        load_game(options.save_file)

    random.seed(GC.random_seed)


    uname = 'Taimor'
    usex = 'Male'
    urace = 'Human'
    urole = 'Wizard'
    
    pygame.display.set_caption('{0} - {1} the {2} {3} {4}'.format(GAME_TITLE, uname, usex, urace, urole))

    
    # Prepare game objects
    GC.clock = pygame.time.Clock()

       
    init_gv()
    GV.screen = pygame.display.set_mode((GV.screen_pw, GV.screen_ph))

    GV.map_surf = pygame.Surface((GV.map_pw, GV.map_ph)).convert()
    GV.alert_surf = pygame.Surface((GV.alert_pw, GV.alert_ph)).convert()
    GV.text_surf = pygame.Surface((GV.text_pw, GV.text_ph)).convert()
    GV.eq_surf = pygame.Surface((GV.eq_pw, GV.eq_ph)).convert()
    GV.status_surf = pygame.Surface((GV.status_pw, GV.status_ph)).convert()

    # Set the system icon
    system_icon = load_image('icon.xpm')
    pygame.display.set_icon(system_icon)
    
    GV.tiles_img = load_image('tiles16.xpm')
    GV.gray_tiles_img = load_image('tiles16_gray.xpm')
    GV.tile_dict = create_tile_dict()
    GV.blank_tile = create_tile(GV.tiles_img, "cmap, wall, dark")

    GC.u = Player(0, 0, 'wizard')
    
    # Create a dlevel
#    GC.map = gen_sparse_maze(MAP_W, MAP_H, 0.1)
#    GC.map = gen_perfect_maze(MAP_W, MAP_H)
    GC.map = gen_connected_rooms()
    GC.u.set_fov_map(GC.map)

    

    message("Welcome, {0}!".format(uname), GV.gold)


    # Have to call this once to before drawing the initial screen.
    GC.u.fov_map.do_fov(GC.u.x, GC.u.y, 10)

    if options.save_file:
        run_history()
    
#    GC.u.fov_map.do_fov(GC.u.x, GC.u.y, 10)

    # Main loop
    while GC.state != 'exit':
        controller_tick()
        view_tick()
    
if __name__ == '__main__':
    main()
