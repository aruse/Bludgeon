import pygame
from pygame.locals import *

from const import *
from game import *
from util import *

# FIXME: temporary
INVENTORY_WIDTH = 50

BUTTON_L = 1
BUTTON_M = 2
BUTTON_R = 3


def menu(header, options, width):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')
 
    #calculate total height for the header (after auto-wrap) and one line per option
#    header_height = libtcod.console_height_left_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
    # FIXME: wordwrap the header
    header_height = 1
    height = len(options) + header_height
 
    #create an off-screen console that represents the menu's window
    GV.window_surf = pygame.Surface((width * GV.font_pw, height * GV.font_ph)).convert()
 
    #print the header, with auto-wrap
    write_text(GV.window_surf, header, 0, justify='left')
 
    #print all the options
    y = header_height
    letter_index = ord('a')
    for option in options:
        text = '(' + chr(letter_index) + ') ' + option
        write_text(GV.window_surf, text, y, justify='left')
        y += 1
        letter_index += 1
 
    GV.window_px = GV.screen_pw / 2 - (width * GV.font_pw) / 2
    GV.window_py = GV.screen_ph / 2 - (height * GV.font_ph) / 2

    GC.menu_options = options
    GC.state = 'menu'
 
def inventory_menu(header):
    inv = GC.u.inventory
    
    if len(inv) == 0:
        options = ['Inventory is empty.']
    else:
        options = [i.name for i in inv]
 
    menu(header, options, INVENTORY_WIDTH)
 

def target_tile(max_range=None):
    """Return the position of a tile left-clicked in player's FOV (optionally in a range), or (None,None) if right-clicked."""
    button = None
    while button is None:
        #render the screen. this erases the inventory and shows the names of objects under the mouse.
        view_tick()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                button = event.button
                break

    x, y = pygame.mouse.get_pos()
    x, y = mouse_coords_to_map_coords(x, y)

    if button == BUTTON_R:
#    or key.vk == libtcod.KEY_ESCAPE:
        return (None, None)  #cancel if the player right-clicked or pressed Escape
 
         #accept the target if the player clicked in FOV, and in case a range is specified, if it's in that range
    if (button == BUTTON_L and GC.u.fov_map.lit(x, y) and
        (max_range is None or GC.u.distance(x, y) <= max_range)):
        return (x, y)
    else:
        return (None, None)

def mouse_coords_to_map_coords(x, y):
    # Compensate for the relative position of the map surface.
    y -= GV.map_py
    # Convert into map coords
    x /= TILE_PW
    y /= TILE_PH
    return x, y
    
def tile_under_mouse():
    """Return the name of the top tile under the mouse."""
    x, y = pygame.mouse.get_pos()
    x, y = mouse_coords_to_map_coords(x, y)
    
    if x > 0 and y > 0 and (
        GC.u.fov_map.lit(x, y) or GC.map[x][y].explored):
    
        for m in GC.monsters + [GC.u]:
            if m.x == x and m.y == y:
                return m.name

        for i in GC.items:
            if i.x == x and i.y == y:
                return i.name

        return GC.map[x][y].name
    else:
        return None

def update_alert_surf():
    GV.alert_surf.fill(GV.black)
    name = tile_under_mouse()
    if name:
        text_img = GV.font.render('You see: ' + tile_under_mouse(), True, GV.gold)
        textpos = text_img.get_rect()
        textpos.centerx = GV.alert_surf.get_rect().width / 2
        textpos.top = 0
        GV.alert_surf.blit(text_img, textpos)


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


    
def write_text(surf, text, line_num, justify='center', column=None, color=GV.default_font_color, antialias=True):
    """Output text to the surface.
    Column can be one of (None, 0, 1, 2, 3)"""
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
    
    write_text(surf, 'Andy the Human Male Apprentice (Chaotic)', 0.5, justify='center')
    write_text(surf, 'Dungeons of Doom, Level 1', 1.5, justify='center')

    write_text(surf, 'HP', 3, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 3 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.hp, GC.u.max_hp, GV.hp_bar_color, GV.hp_bar_bg_color)
    write_text(surf, str(GC.u.hp) + ' / ' + str(GC.u.max_hp), 3, justify='center', column=2)
    
    write_text(surf, 'MP', 4, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 4 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.mp, GC.u.max_mp, GV.mp_bar_color, GV.mp_bar_bg_color)
    write_text(surf, str(GC.u.mp) + ' / ' + str(GC.u.max_mp), 4, justify='center', column=2)

    write_text(surf, 'XP', 5, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 5 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.xp, GC.u.xp_next_level, GV.xp_bar_color, GV.xp_bar_bg_color)
    write_text(surf, str(GC.u.xp) + ' / ' + str(GC.u.xp_next_level), 5, justify='center', column=2)

    write_text(surf, 'Weight', 6, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 6 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.weight, GC.u.burdened, GV.gray, GV.darker_gray)
    write_text(surf, str(GC.u.weight) + ' / ' + str(GC.u.burdened), 6, justify='center', column=2)

    write_text(surf, 'Hunger', 7, justify='left', column=0)
    draw_bar(surf, rect.width / 4,
             rect.top + 7 * GV.font_ph, rect.width *.75 - GV.font_pw,
             GC.u.hunger, GC.u.max_hunger, GV.gray, GV.darker_gray)
    write_text(surf, str(GC.u.hunger) + ' / ' + str(GC.u.max_hunger), 7, justify='center', column=2)
    
    write_text(surf, 'Str', 8, justify='right', column=0)
    write_text(surf, 'Con', 9, justify='right', column=0)
    write_text(surf, 'Dex', 10, justify='right', column=0)
    write_text(surf, 'Int', 11, justify='right', column=0)
    write_text(surf, 'Wis', 12, justify='right', column=0)
    write_text(surf, 'Cha', 13, justify='right', column=0)
    write_text(surf, str(18), 8, justify='left', column=1)
    write_text(surf, str(18), 9, justify='left', column=1)
    write_text(surf, str(18), 10, justify='left', column=1)
    write_text(surf, str(18), 11, justify='left', column=1)
    write_text(surf, str(18), 12, justify='left', column=1)
    write_text(surf, str(18), 13, justify='left', column=1)

    write_text(surf, 'AC', 8, justify='right', column=2)
    write_text(surf, 'Gold', 9, justify='right', column=2)
    write_text(surf, 'Level', 10, justify='right', column=2)
    write_text(surf, 'Time', 11, justify='right', column=2)
    write_text(surf, 'Score', 12, justify='right', column=2)
    write_text(surf, 'Weap Skill', 13, justify='right', column=2)
    write_text(surf, str(18), 8, justify='left', column=3)
    write_text(surf, str(18), 9, justify='left', column=3)
    write_text(surf, str(18), 10, justify='left', column=3)
    write_text(surf, str(18), 11, justify='left', column=3)
    write_text(surf, str(18), 12, justify='left', column=3)
    write_text(surf, str(18), 13, justify='left', column=3)

    write_text(surf, 'Weapon Damage 3d8 + ' + str(6), 14, justify='left')
    write_text(surf, 'Weapon Range ' + str(5), 15, justify='left')
    write_text(surf, 'Hungry Burdened Afraid', 16, justify='left')
    write_text(surf, 'Hallucinating Sick Invisible', 17, justify='left')


def update_text_surf():
    """Update the text buffer."""
    GV.text_surf.fill(GV.text_bg_color)

    i = MAX_MSGS - 1
    for (line, color) in GC.msgs:
        text_img = GV.font.render(line, True, color)
        textpos = text_img.get_rect()
        textpos.left = GV.text_surf.get_rect().left + GV.font_pw
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

    # Always draw the player
    GC.u.draw()
        
def view_tick():
    """Handle all of the view actions in the game loop."""
    update_text_surf()
    update_eq_surf()
    update_status_surf()
    update_alert_surf()
    
    draw_map()
    draw_objects()

    # Draw everything
    GV.screen.blit(GV.map_surf, (GV.map_px, GV.map_py))
    GV.screen.blit(GV.alert_surf, (GV.alert_px, GV.alert_py))
    GV.screen.blit(GV.eq_surf, (GV.eq_px, GV.eq_py))
    GV.screen.blit(GV.status_surf, (GV.status_px, GV.status_py))
    GV.screen.blit(GV.text_surf, (GV.text_px, GV.text_py))

    if GC.state == 'menu':
        GV.screen.blit(GV.window_surf, (GV.window_px, GV.window_py))

    pygame.display.flip()
