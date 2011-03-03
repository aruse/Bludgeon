import pygame
from pygame.locals import *

from const import *
from game import *
from util import *

# FIXME: temporary
INVENTORY_WIDTH = 50


def draw_box(x, y, color=GV.white):
    """Draw a box around the cell at the given coords."""
    pygame.draw.rect(GV.map_surf, color, Rect(x * TILE_W, y * TILE_H, TILE_W, TILE_H), 1)


def menu(header, options, width):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')
 
    # Create the header, with wordwrap
    text_img = wordwrap_img(header, width * GV.font_w, True, GV.default_font_color, justify='left')

    header_height = text_img.get_height() / GV.font_h
    height = len(options) + header_height

    # Create an off-screen console that represents the menu's window
    GV.window_surf = pygame.Surface((width * GV.font_w, height * GV.font_h)).convert()

    # Blit the header
    GV.window_surf.blit(text_img, (0, 0))

    # Blit all the options
    y = header_height
    letter_index = ord('a')
    for option in options:
        text = '(' + chr(letter_index) + ') ' + option
        write_text(GV.window_surf, text, y, justify='left')
        y += 1
        letter_index += 1
 
    GV.window_x = GV.screen_w / 2 - (width * GV.font_w) / 2
    GV.window_y = GV.screen_h / 2 - (height * GV.font_h) / 2

    GC.menu_options = options
    GC.state = ST_MENU
 
def inventory_menu(header):
    inv = GC.u.inventory
    
    if len(inv) == 0:
        options = ['Inventory is empty.']
    else:
        options = [i.name for i in inv]
 
    menu(header, options, INVENTORY_WIDTH)
 
    
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


def wordwrap_img(text, w, antialias, color, justify='left'):
    """Return a surface with the rendered text on it, wordwrapped to fit the given pixel width."""

    lines = []
    line = ""
    words = text.split(' ')

    for word in words:
        test_line = line + word + " "

        if GV.font.size(test_line)[0] < w:
            line = test_line
        else:
            lines.append(line)
            line = word + " "

    lines.append(line)


    rendered_lines = []
    total_h = 0
    for line in lines:
        text_img = GV.font.render(line, antialias, color)
        rendered_lines.append(text_img)
        total_h += text_img.get_height()

    # This surface needs to have a transparent background
    # like all of the surfaces in rendered_lines.
    final_surf = pygame.Surface((w, total_h), SRCALPHA,
                                rendered_lines[0]).convert_alpha()

    y = 0
    for line in rendered_lines:
        if justify == 'left':
            x = 0
        elif justify == 'right':
            x = w - line.get_width()
        else: # justify == 'center'
            x = w / 2 - line.get_width() / 2

        final_surf.blit(line, (x, y))
        y += line.get_height()

    return final_surf

def render_tooltips():
    pass

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
    GV.eq_surf.blit(GV.tiles_img, GV.eq_head, GV.tile_dict['conical hat'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_eyes, GV.tile_dict['lenses'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_neck, GV.tile_dict['oval'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_quiver, GV.tile_dict['runed dagger'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_shirt, GV.tile_dict['T-shirt'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_armor, GV.tile_dict['red dragon scale mail'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_cloak, GV.tile_dict['faded pall'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_rweap, GV.tile_dict['athame'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_hands, GV.tile_dict['riding gloves'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_lweap, GV.tile_dict['long sword'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_rring, GV.tile_dict['diamond'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_lring, GV.tile_dict['wire'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_boots, GV.tile_dict['snow boots'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_light, GV.tile_dict['candle'])


    
def write_text(surf, text, line_num, justify='left', column=None, color=GV.default_font_color, antialias=True):
    """Output text to the surface.
    Column can be one of (None, 0, 1, 2, 3)"""
    rect = surf.get_rect()

    col_width = rect.width / 4
    
    if column is None:
        # Leave a space of one character on the left and right of the surface
        left_border = rect.left + GV.font_w
        right_border = rect.right - GV.font_w
        center = rect.width / 2
    else:
        left_border = rect.left + column * col_width + GV.font_w
        right_border = rect.right - ((3 - column) * col_width) - GV.font_w
        center = (left_border + right_border) / 2
    
    text_img = GV.font.render(text, antialias, color)
    textpos = text_img.get_rect()
    if justify == 'left':
        textpos.left = left_border
    elif justify == 'right':
        textpos.right = right_border
    else: # justify == 'center':
        textpos.centerx = center

    textpos.top = surf.get_rect().top + line_num * GV.font_h
    surf.blit(text_img, textpos)


def render_bar(surf, x, y, length, value, max_value, bar_color, background_color):
    # Render a bar (HP, experience, etc).
    bar_length = int(float(value) / max_value * length)
 
    surf.fill(background_color, rect=pygame.Rect(x, y, length, GV.font_h - 1))
    if bar_length > 0:
        surf.fill(bar_color, rect=pygame.Rect(x, y, bar_length, GV.font_h - 1))
 
    
def update_status_surf():
    """Update the status surface."""
    surf = GV.status_surf
    rect = surf.get_rect()
    surf.fill(GV.text_bg_color)
    y = 0.5
    
    write_text(surf, 'Taimor the Human Male Apprentice (Chaotic)', 0.5, justify='center')
    y += 1
    write_text(surf, 'Dungeons of Doom, Level 1', 1.5, justify='center')
    y += 1.5
    write_text(surf, 'HP', y, justify='left', column=0)
    render_bar(surf, rect.width / 4,
             rect.top + y * GV.font_h, rect.width * .75 - GV.font_w,
             GC.u.hp, GC.u.max_hp, GV.hp_bar_color, GV.hp_bar_bg_color)
    write_text(surf, str(GC.u.hp) + ' / ' + str(GC.u.max_hp), y, justify='center', column=2)
    y += 1
    write_text(surf, 'MP', y, justify='left', column=0)
    render_bar(surf, rect.width / 4,
             rect.top + y * GV.font_h, rect.width * .75 - GV.font_w,
             GC.u.mp, GC.u.max_mp, GV.mp_bar_color, GV.mp_bar_bg_color)
    write_text(surf, str(GC.u.mp) + ' / ' + str(GC.u.max_mp), y, justify='center', column=2)
    y += 1
    write_text(surf, 'XP', y, justify='left', column=0)
    render_bar(surf, rect.width / 4,
             rect.top + y * GV.font_h, rect.width * .75 - GV.font_w,
             GC.u.xp, GC.u.xp_next_level, GV.xp_bar_color, GV.xp_bar_bg_color)
    write_text(surf, str(GC.u.xp) + ' / ' + str(GC.u.xp_next_level), y, justify='center', column=2)
    y += 1
    write_text(surf, 'Weight', y, justify='left', column=0)
    render_bar(surf, rect.width / 4,
             rect.top + y * GV.font_h, rect.width * .75 - GV.font_w,
             GC.u.weight, GC.u.burdened, GV.gray, GV.darker_gray)
    write_text(surf, str(GC.u.weight) + ' / ' + str(GC.u.burdened), y, justify='center', column=2)
    y += 1
    write_text(surf, 'Hunger', y, justify='left', column=0)
    render_bar(surf, rect.width / 4,
             rect.top + y * GV.font_h, rect.width * .75 - GV.font_w,
             GC.u.hunger, GC.u.max_hunger, GV.gray, GV.darker_gray)
    write_text(surf, str(GC.u.hunger) + ' / ' + str(GC.u.max_hunger), y, justify='center', column=2)
    y += 1
    write_text(surf, 'Str', y, justify='right', column=0)
    write_text(surf, str(18), y, justify='left', column=1)
    write_text(surf, 'AC', y, justify='right', column=2)
    write_text(surf, str(18), y, justify='left', column=3)
    y += 1    
    write_text(surf, 'Con', y, justify='right', column=0)
    write_text(surf, str(18), y, justify='left', column=1)
    write_text(surf, 'Gold', y, justify='right', column=2)
    write_text(surf, str(18), y, justify='left', column=3)
    y += 1    
    write_text(surf, 'Dex', y, justify='right', column=0)
    write_text(surf, str(18), y, justify='left', column=1)
    write_text(surf, 'Level', y, justify='right', column=2)
    write_text(surf, str(18), y, justify='left', column=3)
    y += 1    
    write_text(surf, 'Int', y, justify='right', column=0)
    write_text(surf, str(18), y, justify='left', column=1)
    write_text(surf, 'Time', y, justify='right', column=2)
    write_text(surf, str(18), y, justify='left', column=3)
    y += 1    
    write_text(surf, 'Wis', y, justify='right', column=0)
    write_text(surf, str(18), y, justify='left', column=1)
    write_text(surf, 'Score', y, justify='right', column=2)
    write_text(surf, str(18), y, justify='left', column=3)
    y += 1    
    write_text(surf, 'Cha', y, justify='right', column=0)
    write_text(surf, str(18), y, justify='left', column=1)
    write_text(surf, 'Weap Skill', y, justify='right', column=2)
    write_text(surf, str(18), y, justify='left', column=3)

    y += 1    
    write_text(surf, 'Weapon Damage 3d8 + ' + str(6), y, justify='left')
    y += 1    
    write_text(surf, 'Weapon Range ' + str(5), y, justify='left')
    y += 1    
    write_text(surf, 'Hungry Burdened Afraid', y, justify='left')
    y += 1    
    write_text(surf, 'Hallucinating Sick Invisible', y, justify='left')


def update_text_surf():
    """Update the text buffer."""
    GV.text_surf.fill(GV.text_bg_color)

    y = GV.text_h
    for (line, color) in reversed(GC.msgs):
        text_img = wordwrap_img(line, GV.text_w - GV.font_w, True, color, justify='left')
        textpos = text_img.get_rect()
        y -= textpos.height

        # y needs to be able to go negative in order to properly render 
        # multi-line text at the top of the surface.  However, there's no 
        # need for it to get so negative that it would be rendering text
        # completely off the top.
        if y < -GV.text_h:
            break

        textpos.top = y
        textpos.left = GV.text_surf.get_rect().left + GV.font_w
        GV.text_surf.blit(text_img, textpos)


def render_map():
    for x in range(MAP_W):
        for y in range(MAP_H):
            if GC.u.fov_map.lit(x, y):
                GV.map_surf.blit(GV.tiles_img, (x * TILE_W, y * TILE_H), GC.map[x][y].tile)
                GC.map[x][y].explored = True
            else:
                if GC.map[x][y].explored:
                    GV.map_surf.blit(GV.gray_tiles_img, (x * TILE_W, y * TILE_H), GC.map[x][y].tile)
                else:
                    GV.map_surf.blit(GV.tiles_img, (x * TILE_W, y * TILE_H), GV.blank_tile)

    
def render_objects():
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

def render_decorations():
    draw_box(GC.u.x, GC.u.y, GV.white)

        
def view_tick():
    """Handle all of the view actions in the game loop."""
    update_text_surf()
    update_eq_surf()
    update_status_surf()
    update_alert_surf()
    
    render_map()
    render_objects()
    render_decorations()

    # Draw everything
    GV.screen.blit(GV.map_surf, (GV.map_x, GV.map_y))
    GV.screen.blit(GV.alert_surf, (GV.alert_x, GV.alert_y))
    GV.screen.blit(GV.eq_surf, (GV.eq_x, GV.eq_y))
    GV.screen.blit(GV.status_surf, (GV.status_x, GV.status_y))
    GV.screen.blit(GV.text_surf, (GV.text_x, GV.text_y))

    if GC.state == ST_MENU:
        GV.screen.blit(GV.window_surf, (GV.window_x, GV.window_y))
    else:
        render_tooltips()

    pygame.display.flip()
