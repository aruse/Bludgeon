#!/usr/bin/env python

# Copyright (c) 2011, Andy Ruse

import os
import time
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
import color

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
            pass
        elif event.type == MOUSEBUTTONUP:
            pass

        handle_actions()


def monsters_take_turn():
    for m in GC.monsters:
        if m.ai:
            m.ai.take_turn()
        
def handle_actions():
    # If an action has already been taken this clock cycle, don't do another one.
    if GC.action_handled:
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
                
    if u_took_turn:
        GC.fov_recompute = True
        monsters_take_turn()
    else:
        GC.fov_recompute = False
        
    GC.action_handled = True
        

def controller_tick():
    """Handle all of the controller actions in the game loop."""
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




def main():
    # Initializing these modules separately instead of calling pygame.init() is WAY faster.
    pygame.display.init()
    pygame.font.init()

    uname = 'Taimor'
    usex = 'Male'
    urace = 'Human'
    urole = 'Wizard'
    
    pygame.display.set_caption('{0} - {1} the {2} {3} {4}'.format(GAME_TITLE, uname, usex, urace, urole))

    GV.screen = pygame.display.set_mode((GV.screen_pw, GV.screen_ph))

    # Set the system icon
    system_icon = load_image('icon.xpm')
    pygame.display.set_icon(system_icon)

    # Create the backgound
    GV.background = pygame.Surface(GV.screen.get_size()).convert()
    GV.background.fill(color.black)
    
    # Display the background
    GV.screen.blit(GV.background, (0, 0))
    pygame.display.flip()

    # Prepare game objects
    GC.clock = pygame.time.Clock()

    GV.tiles_img = load_image('tiles16.xpm')
    GV.gray_tiles_img = load_image('tiles16_gray.xpm')
    GV.tile_dict = create_tile_dict()
    
    GC.u = Monster(0, 0, 'wizard')
#    GC.monsters.append(Monster(0, 2, 'Beholder',
#                                ai=None))
    
    # Create a dlevel
#    GC.map = gen_sparse_maze(MAP_W, MAP_H, 0.1)
#    GC.map = gen_perfect_maze(MAP_W, MAP_H)
    GC.map = gen_connected_rooms()
    GC.u.set_fov_map(GC.map)
    
    GV.map_surf = pygame.Surface((GV.map_pw, GV.map_ph)).convert()
    GV.text_surf = pygame.Surface((GV.text_pw, GV.text_ph)).convert()
    GV.eq_surf = pygame.Surface((GV.eq_pw, GV.eq_ph)).convert()
    GV.status_surf = pygame.Surface((GV.status_pw, GV.status_ph)).convert()

    GV.font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)

    GV.blank_tile = create_tile(GV.tiles_img, "cmap, wall, dark")

    # Have to call this once to draw the initial screen before the user has inputted anything.
    GC.u.fov_map.do_fov(GC.u.x, GC.u.y, 10)
    
    # Main loop
    while GC.state != 'exit':
        controller_tick()
        view_tick()
    
if __name__ == '__main__':
    main()
