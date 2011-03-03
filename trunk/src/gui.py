import pygame
from pygame.locals import *

from const import *
from game import *
from util import *

# FIXME: temporary
INVENTORY_W = 50


def resize_window():
    """Set the rect dimensions for the window surface."""
    GV.window_rect.x = GV.screen_rect.w / 2 - (GV.window_rect.w * GV.font_w) / 2
    GV.window_rect.y = GV.screen_rect.h / 2 - (GV.window_rect.h * GV.font_h) / 2
    if GV.window_rect.x < 0:
        GV.window_rect.x = 0
    if GV.window_rect.y < 0:
        GV.window_rect.y = 0


def mouse_coords_to_map_coords(x, y):
    # Compensate for the relative position of the map surface.
    x -= GV.map_rect.x
    y -= GV.map_rect.y
    # Convert into map coords
    x /= TILE_W
    y /= TILE_H

    if x < 0 or x > MAP_W - 1:
        x = None
    if y < 0 or y > MAP_H - 1:
        y = None
    return x, y

def draw_box(x, y, color=GV.white):
    """Draw a box around the cell at the given coords."""
    pygame.draw.rect(GV.map_surf, color, Rect(x * TILE_W, y * TILE_H, TILE_W, TILE_H), 1)


def menu(header, options, w):
    # Create the header, with wordwrap
    text_img = wordwrap_img(header, w * GV.font_w, True, GV.default_font_color, justify='left')

    header_h = text_img.get_height() / GV.font_h
    h = len(options) + header_h

    # Create an off-screen console that represents the menu's window
    GV.window_surf = pygame.Surface((w * GV.font_w, h * GV.font_h),
                                    ).convert()
    GV.window_surf.fill(GV.black)
    
    # Blit the header
    GV.window_surf.blit(text_img, (0, 0))

    # Blit all the options
    y = header_h
    letter_index = ord('a')
    for option in options:
        text = '(' + chr(letter_index) + ') ' + option
        write_text(GV.window_surf, text, y, justify='left')
        y += 1
        letter_index += 1
 
    GV.window_rect.w, GV.window_rect.h = w, h
    resize_window()

    GC.menu_options = options
    GC.state = ST_MENU
 
def inventory_menu(header):
    inv = GC.u.inventory
    
    if len(inv) == 0:
        options = ['Inventory is empty.']
    else:
        options = [i.name for i in inv]
 
    menu(header, options, INVENTORY_W)
 
    
def tile_under_mouse():
    """Return the name of the top tile under the mouse."""
    x, y = pygame.mouse.get_pos()
    x, y = mouse_coords_to_map_coords(x, y)

    if x is not None and y is not None and (
        GC.u.fov_map.lit(x, y) or GC.map[x][y].explored):
    
        for m in GC.monsters + [GC.u]:
            if m.x == x and m.y == y:
                return m.name

        for i in GC.items:
            if i.x == x and i.y == y:
                return i.name
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


def add_window_border(surf):
    rect = surf.get_rect()

    left_x, right_x = 0, rect.w - TILE_W
    top_y, bottom_y = 0, rect.h - TILE_H
    
    for x in range(1, rect.w / TILE_W):
        surf.blit(GV.tiles_img, (x * TILE_W, top_y), GV.tile_dict['explosion, fiery, top center'])
        surf.blit(GV.tiles_img, (x * TILE_W, bottom_y), GV.tile_dict['explosion, fiery, bottom center'])
    for y in range(1, rect.h / TILE_H):
        surf.blit(GV.tiles_img, (left_x, y * TILE_H), GV.tile_dict['explosion, fiery, middle left'])
        surf.blit(GV.tiles_img, (right_x, y * TILE_H), GV.tile_dict['explosion, fiery, middle right'])
    
    surf.blit(GV.tiles_img, (left_x, top_y), GV.tile_dict['explosion, fiery, top left'])
    surf.blit(GV.tiles_img, (right_x, top_y), GV.tile_dict['explosion, fiery, top right'])
    surf.blit(GV.tiles_img, (left_x, bottom_y), GV.tile_dict['explosion, fiery, bottom left'])
    surf.blit(GV.tiles_img, (right_x, bottom_y), GV.tile_dict['explosion, fiery, bottom right'])


def render_tooltips():
    name = tile_under_mouse()
    if name:
        text_img = GV.font.render('You see: ' + tile_under_mouse(), True, GV.white)
        textpos = text_img.get_rect()

        tooltip_surf = pygame.Surface((textpos.w + TILE_W * 2, textpos.h + TILE_H * 2),
                                      ).convert()
#        tooltip_surf = pygame.Surface((textpos.w + TILE_W * 2, textpos.h + TILE_H * 2),
#                                      SRCALPHA, 30).convert_alpha()
        tooltip_surf.fill(GV.black)
        textpos.left = TILE_W
        textpos.top = TILE_H
        tooltip_surf.blit(text_img, textpos)

        rect = tooltip_surf.get_rect()
        x, rect.bottom = pygame.mouse.get_pos()

        # The lower left corner of the tooltip is next to the mouse, unless
        # doing so would print the tooltip off the right side of the screen.
        if x + rect.w > GV.screen_rect.w:
            rect.right = x
        else:
            rect.left = x

        add_window_border(tooltip_surf)
        tooltip_surf.set_colorkey(GV.floor_blue)
        tooltip_surf.set_alpha(TOOLTIP_ALPHA)
        GV.screen.blit(tooltip_surf, rect)


def update_eq_surf():
    """Update the equipment surface, displaying what I'm wearing and the most
    valuable gear in my backpack."""
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


    x = 0
    y = GV.eq_boots[1] + TILE_W * 1.5
    for i in GC.u.inventory:
        GV.eq_surf.blit(GV.tiles_img, (x, y), GV.tile_dict[i.name])
        x += TILE_W
        if x > GV.eq_rect.w - TILE_W:
            x = 0
            y += TILE_H
        if y > GV.eq_rect.h - TILE_H:
            break


    
def write_text(surf, text, line_num, justify='left', column=None, color=GV.default_font_color, antialias=True):
    """Output text to the surface.
    Column can be one of (None, 0, 1, 2, 3)"""
    rect = surf.get_rect()

    col_w = rect.w / 4
    
    if column is None:
        # Leave a space of one character on the left and right of the surface
        left_border = rect.left + GV.font_w
        right_border = rect.right - GV.font_w
        center = rect.w / 2
    else:
        left_border = rect.left + column * col_w + GV.font_w
        right_border = rect.right - ((3 - column) * col_w) - GV.font_w
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
    surf.fill(GV.log_bg_color)
    y = 0.5
    
    write_text(surf, 'Taimor the Human Male Apprentice (Chaotic)', 0.5, justify='center')
    y += 1
    write_text(surf, 'Dungeons of Doom, Level 1', 1.5, justify='center')
    y += 1.5
    write_text(surf, 'HP', y, justify='left', column=0)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
             GC.u.hp, GC.u.max_hp, GV.hp_bar_color, GV.hp_bar_bg_color)
    write_text(surf, str(GC.u.hp) + ' / ' + str(GC.u.max_hp), y, justify='center', column=2)
    y += 1
    write_text(surf, 'MP', y, justify='left', column=0)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
             GC.u.mp, GC.u.max_mp, GV.mp_bar_color, GV.mp_bar_bg_color)
    write_text(surf, str(GC.u.mp) + ' / ' + str(GC.u.max_mp), y, justify='center', column=2)
    y += 1
    write_text(surf, 'XP', y, justify='left', column=0)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
             GC.u.xp, GC.u.xp_next_level, GV.xp_bar_color, GV.xp_bar_bg_color)
    write_text(surf, str(GC.u.xp) + ' / ' + str(GC.u.xp_next_level), y, justify='center', column=2)
    y += 1
    write_text(surf, 'Weight', y, justify='left', column=0)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
             GC.u.weight, GC.u.burdened, GV.gray, GV.darker_gray)
    write_text(surf, str(GC.u.weight) + ' / ' + str(GC.u.burdened), y, justify='center', column=2)
    y += 1
    write_text(surf, 'Hunger', y, justify='left', column=0)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
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


def update_log_surf():
    """Update the log surface."""
    GV.log_surf.fill(GV.log_bg_color)

    y = GV.log_rect.h
    for (line, color) in reversed(GC.msgs):
        text_img = wordwrap_img(line, GV.log_rect.w - GV.font_w, True, color, justify='left')
        textpos = text_img.get_rect()
        y -= textpos.h

        # y needs to be able to go negative in order to properly render 
        # multi-line text at the top of the surface.  However, there's no 
        # need for it to get so negative that it would be rendering text
        # completely off the top.
        if y < -GV.log_rect.h:
            break

        textpos.top = y
        textpos.left = GV.log_surf.get_rect().left + GV.font_w
        GV.log_surf.blit(text_img, textpos)


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


def center_map_x():
    """Helper function for center_map().  Handles the horizontal coordinate."""
    if GV.map_rect.w < GV.mapview_rect.w:
        GV.map_rect.x = GV.mapview_rect.w / 2 - GV.map_rect.w / 2  + GV.mapview_rect.x
    else:
        GV.map_rect.x = ((GV.mapview_rect.w / 2)
                    - (GC.u.x * TILE_W)
                    + GV.mapview_rect.x)

        if GV.map_rect.x > GV.mapview_rect.x:
            GV.map_rect.x = GV.mapview_rect.x
        if GV.map_rect.x < GV.mapview_rect.w - GV.map_rect.w + GV.mapview_rect.x:
            GV.map_rect.x = GV.mapview_rect.w - GV.map_rect.w + GV.mapview_rect.x

def center_map_y():
    """Helper function for center_map().  Handles the vertical coordinate."""
    if GV.map_rect.h < GV.mapview_rect.h:
        GV.map_rect.y = GV.mapview_rect.h / 2 - GV.map_rect.h / 2 + GV.mapview_rect.y
    else:
        GV.map_rect.y = ((GV.mapview_rect.h / 2)
                    - (GC.u.y * TILE_H)
                    + GV.mapview_rect.y)

        if GV.map_rect.y > GV.mapview_rect.y:
            GV.map_rect.y = GV.mapview_rect.y
        if GV.map_rect.y < GV.mapview_rect.h - GV.map_rect.h + GV.mapview_rect.y:
            GV.map_rect.y = GV.mapview_rect.h - GV.map_rect.h + GV.mapview_rect.y


def center_map():
    """Moves the map surface so that the player appears at the center of the 
    mapview.  If the map surface is smaller than the mapview, center the map
    inside of the mapviewinstead.
    """
    center_map_x()
    center_map_y()

        
def view_tick():
    """Handle all of the view actions in the game loop."""
    update_log_surf()
    update_eq_surf()
    update_status_surf()
    
    render_map()
    render_objects()
    render_decorations()


    # Draw all of the game surfaces on to the screen
    GV.screen.blit(GV.log_surf, GV.log_rect)
    GV.screen.blit(GV.eq_surf, GV.eq_rect)
    GV.screen.blit(GV.status_surf, GV.status_rect)
    center_map()

    # Need to fill the mapview area with black because the piece of the
    # map that we draw may not fill up the whole area.
    GV.screen.fill(GV.black, GV.mapview_rect)

    # Partition off a piece of the map_surf and blits it on to the screen
    # at the location specified by the mapview_rect
    GV.screen.blit(GV.map_surf, GV.mapview_rect,
                   Rect(GV.mapview_rect.x - GV.map_rect.x,
                        GV.mapview_rect.y - GV.map_rect.y,
                        GV.mapview_rect.w,
                        GV.mapview_rect.h))

    if GC.state == ST_MENU:
        GV.screen.blit(GV.window_surf, GV.window_rect)
    else:
        render_tooltips()

    pygame.display.flip()
