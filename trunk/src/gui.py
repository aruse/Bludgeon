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

def update_eq_surf():
    """Update the equipment surface."""
    GV.eq_surf.fill(GV.dark_gray)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "conical hat"), GV.eq_head)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "lenses"), GV.eq_eyes)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "oval"), GV.eq_neck)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "runed dagger"), GV.eq_quiver)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "T-shirt"), GV.eq_shirt)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "blue dragon scale mail"), GV.eq_armor)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "faded pall"), GV.eq_cloak)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "athame"), GV.eq_rweap)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "padded gloves"), GV.eq_hands)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "long sword"), GV.eq_lweap)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "obsidian"), GV.eq_rring)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "topaz"), GV.eq_lring)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "combat boots"), GV.eq_boots)
    GV.eq_surf.blit(create_tile(GV.tiles_img, "candle"), GV.eq_light)


    
def write_text(surf, text, antialias, x, y, justify=None, column=None, color=GV.default_font_color):
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


def render_bar(surf, x, y, length, value, max_value, bar_color, background_color):
    # Render a bar (HP, experience, etc).
    bar_length = int(float(value) / max_value * length)
 
    surf.fill(background_color, rect=pygame.Rect(x, y, length, FONT_SIZE))
    if bar_length > 0:
        surf.fill(bar_color, rect=pygame.Rect(x, y, bar_length, FONT_SIZE))
 
    
def update_status_surf():
    """Update the status surface."""
    surf = GV.status_surf
    rect = surf.get_rect()
    surf.fill(GV.text_bg_color)
    column_w = STATUS_W / 2
    
    
    write_text(surf, 'Andy the Human Male Apprentice (Chaotic)', 1, 0, 1, justify='center')
    write_text(surf, 'Dungeons of Doom, Level 1', 1, 0, 2, justify='center')

    write_text(surf, 'HP', 1, 1, 3, justify='left', column=1)
    render_bar(surf, rect.left + 4 * FONT_SIZE, rect.top + 3 * FONT_SIZE, 100, GC.u.hp, GC.u.max_hp, GV.light_red, GV.darker_red)
    write_text(surf, str(GC.u.hp) + '/' + str(GC.u.max_hp), 1, 1, 3, justify='center', column=2)

    
    write_text(surf, 'MP', 1, column_w + 1, 3, justify='left', column=3)
    write_text(surf, str(20) + '/' + str(25), 1, column_w + 1, 3, justify='center', column=4)

    write_text(surf, 'XP', 1, 1, 4, justify='left', column=1)
    write_text(surf, str(10) + '/' + str(5000), 1, 1, 4, justify='center', column=2)
    write_text(surf, 'Weight', 1, column_w + 1, 4, justify='left', column=3)
    write_text(surf, str(20) + '/' + str(1000), 1, column_w + 1, 4, justify='center', column=4)

    write_text(surf, 'Hunger ' + str(20) + '/' + str(1000), 1, column_w + 1, 5)
    
    write_text(surf, 'Str ' + str(18), 1, 1, 6)
    write_text(surf, 'Con ' + str(18), 1, 1, 7)
    write_text(surf, 'Dex ' + str(18), 1, 1, 8)
    write_text(surf, 'Int ' + str(18), 1, 1, 9)
    write_text(surf, 'Wis ' + str(18), 1, 1, 10)
    write_text(surf, 'Cha ' + str(18), 1, 1, 11)
    write_text(surf, 'AC ' + str(20), 1, column_w + 1, 6)
    write_text(surf, 'Gold ' + str(20), 1, column_w + 1, 7)
    write_text(surf, 'Level ' + str(20), 1, column_w + 1, 8)
    write_text(surf, 'Time ' + str(20), 1, column_w + 1, 9)
    write_text(surf, 'Score ' + str(20), 1, column_w + 1, 10)
    write_text(surf, 'Weap Skill ' + str(20), 1, column_w + 1, 11)
    write_text(surf, 'Weapon Damage 3d8 + ' + str(6), 1, 1, 12)
    write_text(surf, 'Weapon Range ' + str(5), 1, 1, 13)
    write_text(surf, 'Hungry Burdened Afraid', 1, 1, 14)
    write_text(surf, 'Hallucinating Sick Invisible', 1, 1, 15)


def update_text_surf():
    """Update the text buffer."""
    GV.text_surf.fill(GV.text_bg_color)

    i = MAX_MSGS - 1
    for (line, color) in GC.msgs:
        text_img = GV.font.render(line, 1, GV.default_font_color)
        textpos = text_img.get_rect()
        textpos.left = GV.text_surf.get_rect().left
        textpos.top = i * FONT_SIZE
        GV.text_surf.blit(text_img, textpos)
        i -= 1

def draw_map():
    for x in range(MAP_W):
        for y in range(MAP_H):
            if GC.u.fov_map.lit(x, y):
                GV.map_surf.blit(GC.map[x][y].tile, (x * TILE_PW, y * TILE_PH))
                GC.map[x][y].explored = True
            else:
                if GC.map[x][y].explored:
                    GV.map_surf.blit(GC.map[x][y].gray_tile, (x * TILE_PW, y * TILE_PH))
                else:
                    GV.map_surf.blit(GV.blank_tile, (x * TILE_PW, y * TILE_PH))

    
def draw_objects():
    for item in GC.items:
        if GC.u.fov_map.lit(item.x, item.y):
            item.draw()
        else:
            if GC.map[item.x][item.y].explored:
                item.draw_gray()

    for m in GC.monsters:
        if GC.u.fov_map.lit(m.x, m.y):
            m.draw()
        else:
            if GC.map[m.x][m.y].explored:
                m.draw_gray()

    # Draw the player
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
