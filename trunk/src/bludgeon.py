#!/usr/bin/env python

import os
import time
import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from object import *
from dlevel import *
from tile import *

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'




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
    for monster in GC.monsters:
        if monster.ai is not None:
            monster.ai()
        
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
            message('You moved up!')
            GC.u.move(DIRH['u'])
            u_took_turn = True
        elif GC.key == K_DOWN or GC.key == K_KP2:
            message('You moved down!')
            GC.u.move(DIRH['d'])
            u_took_turn = True
        elif GC.key == K_LEFT or GC.key == K_KP4:
            GC.u.move(DIRH['l'])
            u_took_turn = True
        elif GC.key == K_RIGHT or GC.key == K_KP6:
            GC.u.move(DIRH['r'])
            u_took_turn = True
        elif GC.key == K_KP7:
            GC.u.move(DIRH['ul'])
            u_took_turn = True
        elif GC.key == K_KP9:
            GC.u.move(DIRH['ur'])
            u_took_turn = True
        elif GC.key == K_KP1:
            GC.u.move(DIRH['dl'])
            u_took_turn = True
        elif GC.key == K_KP3:
            GC.u.move(DIRH['dr'])
            u_took_turn = True
                
    if u_took_turn:
        monsters_take_turn()

    GC.action_handled = True
        
def update_wall_tiles():
    """Goes through a level map and makes sure the correct tiles are used for walls, depending on what's in the adjacent spaces."""
    for x in range(MAP_W):
        for y in range(MAP_H):
            if GC.map[x][y] == 0:
                GC.map[x][y] = Tile("cmap, floor of a room")
            if GC.map[x][y] == 1:
                wall_tile = "cmap, wall, horizontal"
                tee = 0

                if x > 0 and GC.map[x - 1][y] == 1:
                    if y > 0 and GC.map[x][y - 1] == 1 and y < MAP_H - 1 and GC.map[x][y + 1] == 1:
                        wall_tile = "cmap, wall, tee left"
                        tee = 1
                    elif y > 0 and GC.map[x][y - 1] == 1:
                        wall_tile = "cmap, wall, top left corner"
                    elif y < MAP_H - 1 and GC.map[x][y + 1] == 1:
                        wall_tile = "cmap, wall, bottom left corner"
                        
                if x < MAP_W - 1 and GC.map[x + 1][y] == 1:
                    if y > 0 and GC.map[x][y - 1] == 1 and y < MAP_H - 1 and GC.map[x][y + 1] == 1:
                        wall_tile = "cmap, wall, tee right"
                        tee = 1
                    elif y > 0 and GC.map[x][y - 1] == 1:
                        wall_tile = "cmap, wall, top right corner"
                    elif y < MAP_H - 1 and GC.map[x][y + 1] == 1:
                        wall_tile = "cmap, wall, bottom right corner"

                if not tee:
                    if y > 0 and GC.map[x][y - 1] == 1:
                        wall_tile = "cmap, wall, vertical"
                        if x > 0 and GC.map[x - 1][y] == 1 and x < MAP_W - 1 and GC.map[x + 1][y] == 1:
                            wall_tile = "cmap, wall, tee up"
                        elif x > 0 and GC.map[x - 1][y] == 1:
                            wall_tile = "cmap, wall, bottom right corner"
                        elif x < MAP_W - 1 and GC.map[x + 1][y] == 1:
                            wall_tile = "cmap, wall, bottom left corner"
                        
                if y < MAP_H - 1 and GC.map[x][y + 1] == 1:
                    wall_tile = "cmap, wall, vertical"
                    if x > 0 and GC.map[x - 1][y] == 1 and x < MAP_W - 1 and GC.map[x + 1][y] == 1:
                        wall_tile = "cmap, wall, tee down"
                    elif x > 0 and GC.map[x - 1][y] == 1:
                        wall_tile = "cmap, wall, top right corner"
                    elif x < MAP_W - 1 and GC.map[x + 1][y] == 1:
                        wall_tile = "cmap, wall, top left corner"

                if x > 0 and GC.map[x - 1][y] == 1 and x < MAP_W - 1 and GC.map[x + 1][y] == 1 and \
                        y > 0 and GC.map[x][y - 1] == 1 and y < MAP_H - 1 and GC.map[x][y + 1] == 1:
                    wall_tile = "cmap, wall, crosswall"

                GC.map[x][y] = Tile(wall_tile)
            if GC.map[x][y] == 2:
                GC.map[x][y] = Tile("cmap, staircase down")



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



def update_text_surf():
    """Update the text buffer."""
    GV.text_surf.fill(TEXT_BG_CLR)

    i = MAX_MSGS - 1
    for (line, color) in GC.msgs:
        text_img = GV.font.render(line, 1, DEFAULT_FONT_CLR)
        textpos = text_img.get_rect()
        textpos.left = GV.text_surf.get_rect().left
        textpos.top = i * FONT_SIZE
        GV.text_surf.blit(text_img, textpos)
        i -= 1


def update_eq_surf():
    """Update the equipment surface."""
    GV.eq_surf.fill(CLR_D_GREY)
    GV.eq_surf.blit(create_tile("conical hat"), GV.eq_head)
    GV.eq_surf.blit(create_tile("lenses"), GV.eq_eyes)
    GV.eq_surf.blit(create_tile("oval"), GV.eq_neck)
    GV.eq_surf.blit(create_tile("runed dagger"), GV.eq_quiver)
    GV.eq_surf.blit(create_tile("T-shirt"), GV.eq_shirt)
    GV.eq_surf.blit(create_tile("blue dragon scale mail"), GV.eq_armor)
    GV.eq_surf.blit(create_tile("faded pall"), GV.eq_cloak)
    GV.eq_surf.blit(create_tile("athame"), GV.eq_rweap)
    GV.eq_surf.blit(create_tile("padded gloves"), GV.eq_hands)
    GV.eq_surf.blit(create_tile("long sword"), GV.eq_lweap)
    GV.eq_surf.blit(create_tile("obsidian"), GV.eq_rring)
    GV.eq_surf.blit(create_tile("topaz"), GV.eq_lring)
    GV.eq_surf.blit(create_tile("combat boots"), GV.eq_boots)
    GV.eq_surf.blit(create_tile("candle"), GV.eq_light)


    
def write_text(surf, text, antialias, color, x, y, justify=None, column=None):
    """Output text to a surface at x, y block coords.
    If justify is set, ignore x variable.
    Column can be one of (1, 2, 3, 4)"""
        
    text_img = GV.font.render(text, antialias, color)
    textpos = text_img.get_rect()
    if justify == 'center':
        if column:
            textpos.centerx = column * surf.get_width() / 4- (surf.get_width() / 4 - 2)
        else:
            textpos.centerx = surf.get_width() / 2
    elif justify == 'left':
        if column:
            textpos.x = column * surf.get_width() / 4 - (surf.get_width() / 4 - 2) + FONT_SIZE / 2
        else:
            textpos.x = x
    elif justify == 'right':
        if column:
            textpos.x = column * surf.get_width() / 4 - FONT_SIZE / 2 - text_img.get_width()
        else:
            textpos.x = x - text_img.get_width()
    else:
        textpos.left = surf.get_rect().left + x * (FONT_SIZE / 2)
    textpos.top = surf.get_rect().top + y * FONT_SIZE
    surf.blit(text_img, textpos)

    
def update_status_surf():
    """Update the status surface."""
    GV.status_surf.fill(TEXT_BG_CLR)
    column_w = STATUS_W / 2

    
    write_text(GV.status_surf, 'Andy the Human Male Apprentice (Chaotic)', 1, DEFAULT_FONT_CLR, 0, 1, justify='center')
    write_text(GV.status_surf, 'Dungeons of Doom, Level 1', 1, DEFAULT_FONT_CLR, 0, 2, justify='center')

    write_text(GV.status_surf, 'HP', 1, DEFAULT_FONT_CLR, 1, 3, justify='left', column=1)
    write_text(GV.status_surf, str(20) + '/' + str(25), 1, DEFAULT_FONT_CLR, 1, 3, justify='center', column=2)

    write_text(GV.status_surf, 'MP', 1, DEFAULT_FONT_CLR, column_w + 1, 3, justify='left', column=3)
    write_text(GV.status_surf, str(20) + '/' + str(25), 1, DEFAULT_FONT_CLR, column_w + 1, 3, justify='center', column=4)

    write_text(GV.status_surf, 'XP', 1, DEFAULT_FONT_CLR, 1, 4, justify='left', column=1)
    write_text(GV.status_surf, str(10) + '/' + str(5000), 1, DEFAULT_FONT_CLR, 1, 4, justify='center', column=2)
    write_text(GV.status_surf, 'Weight', 1, DEFAULT_FONT_CLR, column_w + 1, 4, justify='left', column=3)
    write_text(GV.status_surf, str(20) + '/' + str(1000), 1, DEFAULT_FONT_CLR, column_w + 1, 4, justify='center', column=4)

    write_text(GV.status_surf, 'Hunger ' + str(20) + '/' + str(1000), 1, DEFAULT_FONT_CLR, column_w + 1, 5)
    
    write_text(GV.status_surf, 'Str ' + str(18), 1, DEFAULT_FONT_CLR, 1, 6)
    write_text(GV.status_surf, 'Con ' + str(18), 1, DEFAULT_FONT_CLR, 1, 7)
    write_text(GV.status_surf, 'Dex ' + str(18), 1, DEFAULT_FONT_CLR, 1, 8)
    write_text(GV.status_surf, 'Int ' + str(18), 1, DEFAULT_FONT_CLR, 1, 9)
    write_text(GV.status_surf, 'Wis ' + str(18), 1, DEFAULT_FONT_CLR, 1, 10)
    write_text(GV.status_surf, 'Cha ' + str(18), 1, DEFAULT_FONT_CLR, 1, 11)
    write_text(GV.status_surf, 'AC ' + str(20), 1, DEFAULT_FONT_CLR, column_w + 1, 6)
    write_text(GV.status_surf, 'Gold ' + str(20), 1, DEFAULT_FONT_CLR, column_w + 1, 7)
    write_text(GV.status_surf, 'Level ' + str(20), 1, DEFAULT_FONT_CLR, column_w + 1, 8)
    write_text(GV.status_surf, 'Time ' + str(20), 1, DEFAULT_FONT_CLR, column_w + 1, 9)
    write_text(GV.status_surf, 'Score ' + str(20), 1, DEFAULT_FONT_CLR, column_w + 1, 10)
    write_text(GV.status_surf, 'Weap Skill ' + str(20), 1, DEFAULT_FONT_CLR, column_w + 1, 11)
    write_text(GV.status_surf, 'Weapon Damage 3d8 + ' + str(6), 1, DEFAULT_FONT_CLR, 1, 12)
    write_text(GV.status_surf, 'Weapon Range ' + str(5), 1, DEFAULT_FONT_CLR, 1, 13)
    write_text(GV.status_surf, 'Hungry Burdened Afraid', 1, DEFAULT_FONT_CLR, 1, 14)
    write_text(GV.status_surf, 'Hallucinating Sick Invisible', 1, DEFAULT_FONT_CLR, 1, 15)


def draw_map():
    for x in range(MAP_W):
        for y in range(MAP_H):
            GV.map_surf.blit(GC.map[x][y].tile,  (x * TILE_PW, y * TILE_PH))
    

def draw_objects():
    for item in GC.items:
        item.draw()

    for monster in GC.monsters:
        monster.draw()

    GC.u.draw()
        
def view_tick():
    """Handle all of the view actions in the game loop."""
    update_text_surf()
    update_eq_surf()
    update_status_surf()

    draw_map()
    draw_objects()

    # Draw everything
    GV.screen.blit(GV.background, (0, 0))
    GV.screen.blit(GV.map_surf, (GV.map_px, GV.map_py))
    GV.screen.blit(GV.eq_surf, (GV.eq_px, GV.eq_py))
    GV.screen.blit(GV.status_surf, (GV.status_px, GV.status_py))
    GV.screen.blit(GV.text_surf, (GV.text_px, GV.text_py))
    pygame.display.flip()

def main():
    pygame.init()
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
    GV.background = pygame.Surface(GV.screen.get_size())
    GV.background = GV.background.convert()
    GV.background.fill(CLR_BLACK)
    
    # Display the background
    GV.screen.blit(GV.background, (0, 0))
    pygame.display.flip()

    # Create a maze
#    GC.map = gen_sparse_maze(MAP_W, MAP_H, 0.1)
    GC.map = gen_perfect_maze(MAP_W, MAP_H)
    GC.map[int(MAP_W / 2)][int(MAP_H / 2)] = 2

    GV.map_surf = pygame.Surface((GV.map_pw, GV.map_ph))
    GV.map_surf = GV.map_surf.convert()

    GV.text_surf = pygame.Surface((GV.text_pw, GV.text_ph))
    GV.text_surf = GV.text_surf.convert()

    GV.eq_surf = pygame.Surface((GV.eq_pw, GV.eq_ph))
    GV.eq_surf = GV.eq_surf.convert()

    GV.status_surf = pygame.Surface((GV.status_pw, GV.status_ph))
    GV.status_surf = GV.status_surf.convert()


    GV.font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)

    # Prepare game objects
    GC.clock = pygame.time.Clock()
    GV.tiles_image = load_image('tiles16.xpm')

    GV.tile_dict = create_tile_dict()
    GV.glyph_dict = create_tile_dict()
    
    GC.u = Monster(0, 0, 'wizard')
    GC.monsters.append(Monster(MAP_W - 1, MAP_H - 1, 'Beholder',
                                ai=None))

    update_wall_tiles()
    
    # Main loop
    while GC.state != 'exit':
        controller_tick()
        view_tick()
                           
if __name__ == '__main__':
    main()
