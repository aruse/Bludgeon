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


    
def write_status_text(text, line_num, justify='center', column=None, color=GV.default_font_color, antialias=True):
    """Output text to the status surface.
    Column can be one of (None, 0, 1, 2, 3)"""
    surf = GV.status_surf
    rect = surf.get_rect()

    col_width = rect.width / 4
    
    if column is None:
        # Leave a space of one character on the left and right of the surface
        left_border = rect.left + GV.font_pw
        right_border = rect.right - GV.font_pw
        center = rect.width / 2
    else:
        left_border = rect.left + column * col_width + GV.font_pw
        right_border = rect.right - ((3 - column) * col_width) - GV.font_pw
        center = (left_border + right_border) / 2
    
    text_img = GV.font.render(text, antialias, color)
    textpos = text_img.get_rect()
    if justify == 'left':
        textpos.left = left_border
    elif justify == 'right':
        textpos.right = right_border
    else: # justify == 'center':
        textpos.centerx = center

    textpos.top = surf.get_rect().top + line_num * GV.font_ph
    surf.blit(text_img, textpos)


def draw_bar(surf, x, y, length, value, max_value, bar_color, background_color):
    # Render a bar (HP, experience, etc).
    bar_length = int(float(value) / max_value * length)
 
    surf.fill(background_color, rect=pygame.Rect(x, y, length, GV.font_ph - 1))
    if bar_length > 0:
        surf.fill(bar_color, rect=pygame.Rect(x, y, bar_length, GV.font_ph - 1))
 
    
def update_status_surf():
    """Update the status surface."""
    surf = GV.status_surf
    rect = surf.get_rect()
    surf.fill(GV.text_bg_color)
    
    write_status_text('Andy the Human Male Apprentice (Chaotic)', 0.5, justify='center')
    write_status_text('Dungeons of Doom, Level 1', 1.5, justify='center')

    write_status_text('HP', 3, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 3 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.hp, GC.u.max_hp, GV.hp_bar_color, GV.hp_bar_bg_color)
    write_status_text(str(GC.u.hp) + ' / ' + str(GC.u.max_hp), 3, justify='center', column=2)
    
    write_status_text('MP', 4, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 4 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.mp, GC.u.max_mp, GV.mp_bar_color, GV.mp_bar_bg_color)
    write_status_text(str(GC.u.mp) + ' / ' + str(GC.u.max_mp), 4, justify='center', column=2)

    write_status_text('XP', 5, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 5 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.xp, GC.u.xp_next_level, GV.xp_bar_color, GV.xp_bar_bg_color)
    write_status_text(str(GC.u.xp) + ' / ' + str(GC.u.xp_next_level), 5, justify='center', column=2)

    write_status_text('Weight', 6, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 6 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.weight, GC.u.burdened, GV.gray, GV.darker_gray)
    write_status_text(str(GC.u.weight) + ' / ' + str(GC.u.burdened), 6, justify='center', column=2)

    write_status_text('Hunger', 7, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 7 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.hunger, GC.u.max_hunger, GV.gray, GV.darker_gray)
    write_status_text(str(GC.u.hunger) + ' / ' + str(GC.u.max_hunger), 7, justify='center', column=2)
    
    write_status_text('Str', 8, justify='right', column=0)
    write_status_text('Con', 9, justify='right', column=0)
    write_status_text('Dex', 10, justify='right', column=0)
    write_status_text('Int', 11, justify='right', column=0)
    write_status_text('Wis', 12, justify='right', column=0)
    write_status_text('Cha', 13, justify='right', column=0)
    write_status_text(str(18), 8, justify='left', column=1)
    write_status_text(str(18), 9, justify='left', column=1)
    write_status_text(str(18), 10, justify='left', column=1)
    write_status_text(str(18), 11, justify='left', column=1)
    write_status_text(str(18), 12, justify='left', column=1)
    write_status_text(str(18), 13, justify='left', column=1)

    write_status_text('AC', 8, justify='right', column=2)
    write_status_text('Gold', 9, justify='right', column=2)
    write_status_text('Level', 10, justify='right', column=2)
    write_status_text('Time', 11, justify='right', column=2)
    write_status_text('Score', 12, justify='right', column=2)
    write_status_text('Weap Skill', 13, justify='right', column=2)
    write_status_text(str(18), 8, justify='left', column=3)
    write_status_text(str(18), 9, justify='left', column=3)
    write_status_text(str(18), 10, justify='left', column=3)
    write_status_text(str(18), 11, justify='left', column=3)
    write_status_text(str(18), 12, justify='left', column=3)
    write_status_text(str(18), 13, justify='left', column=3)

    write_status_text('Weapon Damage 3d8 + ' + str(6), 14, justify='left')
    write_status_text('Weapon Range ' + str(5), 15, justify='left')
    write_status_text('Hungry Burdened Afraid', 16, justify='left')
    write_status_text('Hallucinating Sick Invisible', 17, justify='left')


def update_text_surf():
    """Update the text buffer."""
    GV.text_surf.fill(GV.text_bg_color)

    i = MAX_MSGS - 1
    for (line, color) in GC.msgs:
        text_img = GV.font.render(line, 1, GV.default_font_color)
        textpos = text_img.get_rect()
        textpos.left = GV.text_surf.get_rect().left
        textpos.top = i * GV.font_ph
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
    GV.screen.blit(GV.map_surf, (GV.map_px, GV.map_py))
    GV.screen.blit(GV.eq_surf, (GV.eq_px, GV.eq_py))
    GV.screen.blit(GV.status_surf, (GV.status_px, GV.status_py))
    GV.screen.blit(GV.text_surf, (GV.text_px, GV.text_py))
    pygame.display.flip()
