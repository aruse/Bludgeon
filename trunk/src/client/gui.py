# Copyright (c) 2011, Andy Ruse

import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from widgets import *


def handle_resize(w, h):
    """Shuffle surfaces around to their correct places when the game
    is resized.
    """
    if w < MIN_LOG_W + GV.eq_rect.w + GV.status_rect.w:
        w = MIN_LOG_W + GV.eq_rect.w + GV.status_rect.w
    if h < GV.status_rect.h + MIN_MAPVIEW_H:
        h = GV.status_rect.h + MIN_MAPVIEW_H

    # Resize the main screen
    GV.screen_rect.w, GV.screen_rect.h = w, h
    GV.screen = pygame.display.set_mode((GV.screen_rect.w, GV.screen_rect.h),
                                        pygame.RESIZABLE)

    # Resize the mapview. We have to shave off a little so the scrollbars
    # can fit
    GV.mapview_rect.w = GV.screen_rect.w - SCROLLBAR_W
    GV.mapview_rect.h = GV.screen_rect.h - GV.status_rect.h - SCROLLBAR_W

    # Resize the log surface
    GV.log_rect.w = GV.screen_rect.w - (GV.eq_rect.w + GV.status_rect.w) \
        - SCROLLBAR_W
    GV.logview_rect.w = GV.log_rect.w

    # Resize the dialog surface
    set_dialog_size()

    # Move the surfaces to their new locations
    move_surface_locations()
    GC.log_updated = True

    GV.x_scrollbar.resize()
    GV.y_scrollbar.resize()
    GV.log_scrollbar.resize()

    center_map()

def set_dialog_size():
    """Set the rect dimensions for the dialog surface."""
    GV.dialog_rect.x = GV.screen_rect.w / 2 - GV.dialog_rect.w / 2
    GV.dialog_rect.y = GV.screen_rect.h / 2 - GV.dialog_rect.h / 2
    if GV.dialog_rect.x < 0:
        GV.dialog_rect.x = 0
    if GV.dialog_rect.y < 0:
        GV.dialog_rect.y = 0


def mouse_coords_to_map_coords(x, y):
    # Compensate for the relative position of the map surface.
    x -= GV.map_rect.x
    y -= GV.map_rect.y

    # Compensate for map border
    x -= TILE_W
    y -= TILE_H

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
    coords = cell2pixel(x, y)
    pygame.draw.rect(GV.map_surf, color,
                     Rect((x + 1) * TILE_W, (y + 1) * TILE_H,
                          TILE_W, TILE_H), 1)

def draw_line_between(x1, y1, x2, y2, color=GV.white):
    """Draw a line between the two given adjacent cells."""
    # Horizontal line, (x1, y1) on the left
    if x1 < x2:
        coords1 = cell2pixel(x2, y2)
        coords2 = cell2pixel(x2, y2 + 1)
    # Horizontal line, (x2, y2) on the left
    elif x2 < x1:
        coords1 = cell2pixel(x1, y1)
        coords2 = cell2pixel(x1, y1 + 1)
    # Vertical line, (x1, y1) on the top
    elif y1 < y2:
        coords1 = cell2pixel(x2, y2)
        coords2 = cell2pixel(x2 + 1, y2)
    # Vertical line, (x2, y2) on the top
    elif y2 < y1:
        coords1 = cell2pixel(x1, y1)
        coords2 = cell2pixel(x1 + 1, y1)

    pygame.draw.line(GV.map_surf, color,
                     coords1, coords2, 1)


def img_fill(surf, img, rect=None):
    """Fill the given surface with the given image.  If rect is None, fill the
    whole surface.  Otherwise fill on the rect portion.
    """
    if rect is None:
        rect = surf.get_rect()
    img_rect = img.get_rect()
        
    x, y = 0, 0
    while True:
        # Don't worry about spilling over the edges of the surface.  Pygame
        # will handle it and it won't be a problem unless the image is huge.
        surf.blit(img, (x, y))
        x += img_rect.w

        if x > rect.w:
            x = 0
            y += img_rect.h

        if y > rect.h:
            break


def menu(header, options, w):
    padding = BORDER_W + PADDING

    # Create the header, with wordwrap
    text_img = wordwrap_img(header, w, True, GV.menu_font_color,
                            justify='left')

    header_h = text_img.get_height()
    h = len(options) * GV.font_h + header_h

    # Expand the width to fit long option names
    for option in options:
        text = ' (X) ' + option
        text_w = GV.font.size(text)[0]
        if text_w > w:
            w = text_w

    # Create a new surface on which to draw the menu
    surf_w = w + padding * 2
    surf_h = h + padding * 2
    GV.dialog_surf = pygame.Surface((surf_w, surf_h),
                                    ).convert()
    img_fill(GV.dialog_surf, GV.menu_bg_img,
             Rect(surf_w + padding, surf_h + padding,
                  surf_w - padding * 2, surf_h - padding * 2))

    
    # Blit the header
    GV.dialog_surf.blit(text_img, (BORDER_W + PADDING, BORDER_W + PADDING))

    # Blit all the options
    y = (header_h + padding) / float(GV.font_h)
    letter_index = ord('a')
    for option in options:
        text = ' (' + chr(letter_index) + ') ' + option
        write_text(GV.dialog_surf, text, y, color=GV.menu_font_color,
                   justify='left', padding=padding)
        y += 1
        letter_index += 1

    # Make it pretty
    add_surface_border(GV.dialog_surf)
    GV.dialog_surf.set_colorkey(GV.floor_blue)
#    GV.dialog_surf.set_alpha(TOOLTIP_ALPHA)

    GV.dialog_rect.w, GV.dialog_rect.h = w, h
    set_dialog_size()

    GC.menu_options = options
    GC.state = ST_MENU
 
def inventory_menu(header, menu_type):
    """Display an inventory menu.
    header -- Text to display at the top of the menu.
    menu_type -- Keyword identifying the type of menu.
    """
    GC.menu = menu_type

    inv = GC.u.inventory
    if len(inv) == 0:
        options = ['Inventory is empty.']
    else:
        options = [i.name for i in inv]
 
    menu(header, options, MIN_INVENTORY_W)
 
    
def object_under_mouse():
    """Return the top object under the mouse."""
    x, y = pygame.mouse.get_pos()
    x, y = mouse_coords_to_map_coords(x, y)

    if x is not None and y is not None and (
        GC.u.fov_map.in_fov(x, y) or GC.map[x][y].explored):
    
        for m in GC.monsters + [GC.u]:
            if m.x == x and m.y == y:
                return m

        for i in GC.items:
            if i.x == x and i.y == y:
                return i
    else:
        return None


def wordwrap_img(text, w, antialias, color, justify='left'):
    """Return a surface with the rendered text on it, wordwrapped to
    fit the given pixel width.
    """

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


def add_surface_border(surf):
    rect = surf.get_rect()

    left_x, right_x = 0, rect.w - BORDER_W
    top_y, bottom_y = 0, rect.h - BORDER_W
    
    for x in range(1, rect.w / BORDER_W):
        surf.blit(GV.tiles_img, (x * BORDER_W, top_y),
                  GV.tile_dict['explosion, fiery, top center'])
        surf.blit(GV.tiles_img, (x * BORDER_W, bottom_y),
                  GV.tile_dict['explosion, fiery, bottom center'])
    for y in range(1, rect.h / BORDER_W):
        surf.blit(GV.tiles_img, (left_x, y * BORDER_W),
                  GV.tile_dict['explosion, fiery, middle left'])
        surf.blit(GV.tiles_img, (right_x, y * BORDER_W),
                  GV.tile_dict['explosion, fiery, middle right'])
    
    surf.blit(GV.tiles_img, (left_x, top_y),
              GV.tile_dict['explosion, fiery, top left'])
    surf.blit(GV.tiles_img, (right_x, top_y),
              GV.tile_dict['explosion, fiery, top right'])
    surf.blit(GV.tiles_img, (left_x, bottom_y),
              GV.tile_dict['explosion, fiery, bottom left'])
    surf.blit(GV.tiles_img, (right_x, bottom_y),
              GV.tile_dict['explosion, fiery, bottom right'])


def render_tooltips():
    obj = object_under_mouse()
    if obj:
        if obj.__class__.__name__ == 'Monster':
            hp_bar = True
        else:
            hp_bar = False

        bar_len = 100

        if GC.u.fov_map.in_fov(obj.x, obj.y):
            text = 'You see: ' + obj.name
        else:
            text = 'You remember seeing: ' + obj.name

        text_img = GV.font.render(text, True, GV.white)
        text_rect = text_img.get_rect()

        if hp_bar and text_rect.w < bar_len:
            surf_w = bar_len
        else:
            surf_w = text_rect.w

        surf_w += PADDING * 2 + BORDER_W * 2

        surf_h = text_rect.h + PADDING * 2 + BORDER_W * 2
        if hp_bar:
            surf_h += GV.font_h

        tooltip_surf = pygame.Surface((surf_w, surf_h)).convert()
        tooltip_surf.fill(GV.black)

        text_rect.centerx = surf_w / 2
        text_rect.top = BORDER_W + PADDING
        tooltip_surf.blit(text_img, text_rect)

        if hp_bar:
            render_bar(tooltip_surf,
                       BORDER_W + PADDING,
                       BORDER_W + PADDING + text_rect.h,
                       bar_len, obj.hp, obj.max_hp,
                       GV.hp_bar_color, GV.hp_bar_bg_color)
            hp_img = GV.font.render(str(obj.hp) + ' / ' + str(obj.max_hp),
                                      True, GV.white)
            hp_rect = hp_img.get_rect()
            hp_rect.centerx = BORDER_W + PADDING + bar_len / 2
            hp_rect.top = BORDER_W + PADDING + text_rect.h
            tooltip_surf.blit(hp_img, hp_rect)


        rect = tooltip_surf.get_rect()
        x, rect.bottom = pygame.mouse.get_pos()

        # The lower left corner of the tooltip is next to the mouse, unless
        # doing so would print the tooltip off the right side of the screen.
        if x + rect.w > GV.screen_rect.w:
            rect.right = x
        else:
            rect.left = x

        add_surface_border(tooltip_surf)
        tooltip_surf.set_colorkey(GV.floor_blue)
        tooltip_surf.set_alpha(TOOLTIP_ALPHA)
        GV.screen.blit(tooltip_surf, rect)


def update_eq_surf():
    """Update the equipment surface, displaying what I'm wearing and the most
    valuable gear in my backpack."""
    GV.eq_surf.fill(GV.black)
    GV.eq_surf.blit(GV.tiles_img, GV.eq_head, GV.tile_dict['conical hat'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_eyes, GV.tile_dict['lenses'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_neck, GV.tile_dict['oval'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_quiver, GV.tile_dict['runed dagger'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_shirt, GV.tile_dict['T-shirt'])
    GV.eq_surf.blit(GV.tiles_img, GV.eq_armor,
                    GV.tile_dict['red dragon scale mail'])
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


    
def write_text(surf, text, line_num, justify='left',
               column=None, color=GV.default_font_color,
               antialias=True, padding=0):
    """Output text to the surface.
    Column can be one of (None, 0, 1, 2, 3)"""
    rect = surf.get_rect()

    col_w = rect.w / 4
    
    if column is None:
        left_border = rect.left + padding
        right_border = rect.right - padding
        center = rect.w / 2
    else:
        left_border = rect.left + column * col_w + padding
        right_border = rect.right - ((3 - column) * col_w) - padding
        center = (left_border + right_border) / 2
    
    text_img = GV.font.render(text, antialias, color)
    text_rect = text_img.get_rect()
    if justify == 'left':
        text_rect.left = left_border
    elif justify == 'right':
        text_rect.right = right_border
    else: # justify == 'center':
        text_rect.centerx = center

    text_rect.top = surf.get_rect().top + line_num * GV.font_h
    surf.blit(text_img, text_rect)


def render_bar(surf, x, y, length, value,
               max_value, bar_color, background_color):
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
    
    write_text(surf, 'Taimor the Human Male Apprentice (Chaotic)',
               0.5, justify='center')
    y += 1
    write_text(surf, 'Dungeons of Doom, Level 1', 1.5, justify='center')
    y += 1.5
    write_text(surf, 'HP', y, justify='left', column=0, padding=GV.font_w)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
             GC.u.hp, GC.u.max_hp, GV.hp_bar_color, GV.hp_bar_bg_color)
    write_text(surf, str(GC.u.hp) + ' / ' + str(GC.u.max_hp),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'MP', y, justify='left', column=0, padding=GV.font_w)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
             GC.u.mp, GC.u.max_mp, GV.mp_bar_color, GV.mp_bar_bg_color)
    write_text(surf, str(GC.u.mp) + ' / ' + str(GC.u.max_mp),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'XP', y, justify='left', column=0, padding=GV.font_w)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
             GC.u.xp, GC.u.xp_next_level, GV.xp_bar_color, GV.xp_bar_bg_color)
    write_text(surf, str(GC.u.xp) + ' / ' + str(GC.u.xp_next_level),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'Weight', y, justify='left', column=0, padding=GV.font_w)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
             GC.u.weight, GC.u.burdened, GV.gray, GV.darker_gray)
    write_text(surf, str(GC.u.weight) + ' / ' + str(GC.u.burdened),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'Hunger', y, justify='left', column=0, padding=GV.font_w)
    render_bar(surf, rect.w / 4,
             rect.top + y * GV.font_h, rect.w * .75 - GV.font_w,
             GC.u.hunger, GC.u.max_hunger, GV.gray, GV.darker_gray)
    write_text(surf, str(GC.u.hunger) + ' / ' + str(GC.u.max_hunger),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'Str', y, justify='right', column=0, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=GV.font_w)
    write_text(surf, 'AC', y, justify='right', column=2, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=GV.font_w)
    y += 1    
    write_text(surf, 'Con', y, justify='right', column=0, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=GV.font_w)
    write_text(surf, 'Gold', y, justify='right', column=2, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=GV.font_w)
    y += 1    
    write_text(surf, 'Dex', y, justify='right', column=0, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=GV.font_w)
    write_text(surf, 'Level', y, justify='right', column=2, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=GV.font_w)
    y += 1    
    write_text(surf, 'Int', y, justify='right', column=0, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=GV.font_w)
    write_text(surf, 'Time', y, justify='right', column=2, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=GV.font_w)
    y += 1    
    write_text(surf, 'Wis', y, justify='right', column=0, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=GV.font_w)
    write_text(surf, 'Score', y, justify='right', column=2, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=GV.font_w)
    y += 1    
    write_text(surf, 'Cha', y, justify='right', column=0, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=GV.font_w)
    write_text(surf, 'Weap Skill', y, justify='right',
               column=2, padding=GV.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=GV.font_w)

    y += 1    
    write_text(surf, 'Weapon Damage 3d8 + ' + str(6), y, justify='left',
               padding=GV.font_w)
    y += 1    
    write_text(surf, 'Weapon Range ' + str(5), y, justify='left',
               padding=GV.font_w)
    y += 1    
    write_text(surf, 'Hungry Burdened Confused Poisoned', y, justify='left',
               padding=GV.font_w)
    y += 1    
    write_text(surf, 'Hallucinating Sick Blind Stunned', y, justify='left',
               padding=GV.font_w)

def update_log_surf():
    """Update the log surface."""
    total_h = 0
    text_imgs = []
    for line, color in reversed(GC.msgs):
        text_img = wordwrap_img(line, GV.log_rect.w - GV.font_w,
                                True, color, justify='left')
        text_rect = text_img.get_rect()

        text_imgs.append((text_img, text_rect))
        total_h += text_rect.h

    # To avoid divide-by-zero errors when there are no messages to display.
    if total_h < 1:
        total_h = 1

    GV.log_surf = pygame.Surface((GV.logview_rect.w, total_h)).convert()
    GV.log_surf.fill(GV.log_bg_color)
    GV.log_rect.h = total_h
    GV.log_rect.bottom = GV.logview_rect.bottom

    y = GV.log_rect.h
    for text_img, text_rect in text_imgs:
        y -= text_rect.h
        text_rect.top = y
        text_rect.left = GV.log_surf.get_rect().left + GV.font_w
        GV.log_surf.blit(text_img, text_rect)

    GV.log_scrollbar.resize()
    GV.log_scrollbar.align()

    # Mark the log surface as updated
    GC.log_updated = False
    

def render_map():
    GV.map_surf.fill(GV.black)

    for x in range(MAP_W):
        for y in range(MAP_H):
            if GC.u.fov_map.in_fov(x, y):
                GC.map[x][y].draw(x, y)
                GC.map[x][y].explored = True
            else:
                if GC.map[x][y].explored:
                    GC.map[x][y].draw_gray(x, y)
                else:
                    GV.map_surf.blit(GV.tiles_img,
                                     cell2pixel(x, y), GV.blank_tile)
    
def render_objects():
    for item in GC.items:
        if GC.u.fov_map.in_fov(item.x, item.y):
            item.draw()
        else:
            if GC.map[item.x][item.y].explored:
                item.draw_gray()

    for m in GC.monsters:
        if GC.u.fov_map.in_fov(m.x, m.y):
            m.draw()

    # Always draw the player
    GC.u.draw()


def draw_fov_outline(color):
    """Draws an outline around the outside of any FOV maps in play."""
    for m in GC.monsters + [GC.u]:
        if m.fov_map is None:
            continue

        for x in range(m.x - m.fov_radius, m.x + m.fov_radius):
            for y in range(m.y - m.fov_radius, m.y + m.fov_radius):
                if (m.fov_map.in_fov(x, y)
                    != m.fov_map.in_fov(x + 1, y)):
                    draw_line_between(x, y, x + 1, y, color)
                if (m.fov_map.in_fov(x, y)
                    != m.fov_map.in_fov(x, y + 1)):
                    draw_line_between(x, y, x, y + 1, color)


def render_decorations():
    if GC.state == ST_PLAYING:
        draw_box(GC.u.x, GC.u.y, GV.white)

    if GC.state == ST_TARGETING:
        x, y = pygame.mouse.get_pos()
        x, y = mouse_coords_to_map_coords(x, y)
        draw_box(x, y, GV.white)


    pygame.draw.rect(GV.map_surf, GV.red, Rect(0, 0, GV.map_rect.w, GV.map_rect.h), 1)

    if GC.fov_outline:
        draw_fov_outline(GV.red)

    # Put an image in the corner where the scrollbars intersect
    # FIXME: this doesn't actually do anything
    GV.screen.blit(GV.tiles_img,
                   (GV.mapview_rect.x + GV.mapview_rect.w,
                    GV.mapview_rect.y + GV.mapview_rect.h),
                   GV.tile_dict['Cthulhu'])


def center_map_x():
    """Helper function for center_map().  Handles the horizontal coordinate."""
    if GV.map_rect.w < GV.mapview_rect.w:
        GV.map_rect.x = GV.mapview_rect.w / 2 - GV.map_rect.w / 2 + \
            GV.mapview_rect.x
    else:
        GV.map_rect.x = ((GV.mapview_rect.w / 2)
                         - (GC.u.x * TILE_W)
                         + GV.mapview_rect.x)

        if GV.map_rect.x > GV.mapview_rect.x:
            GV.map_rect.x = GV.mapview_rect.x

        min_x = GV.mapview_rect.w - GV.map_rect.w + GV.mapview_rect.x

        if GV.map_rect.x < min_x:
            GV.map_rect.x = min_x

    # Move the scrollbar slider to the correct position
    GV.x_scrollbar.align()


def center_map_y():
    """Helper function for center_map().  Handles the vertical coordinate."""
    if GV.map_rect.h < GV.mapview_rect.h:
        GV.map_rect.y = GV.mapview_rect.h / 2 - GV.map_rect.h / 2 + \
            GV.mapview_rect.y
    else:
        GV.map_rect.y = ((GV.mapview_rect.h / 2)
                         - (GC.u.y * TILE_H)
                         + GV.mapview_rect.y)

        if GV.map_rect.y > GV.mapview_rect.y:
            GV.map_rect.y = GV.mapview_rect.y

        min_y = GV.mapview_rect.h - GV.map_rect.h + GV.mapview_rect.y
        if GV.map_rect.y < min_y:
            GV.map_rect.y = min_y

    # Move the scrollbar slider to the correct position
    GV.y_scrollbar.align()

def center_map():
    """Moves the map surface so that the player appears at the center of the 
    mapview.  If the map surface is smaller than the mapview, center the map
    inside of the mapview instead.
    """
    center_map_x()
    center_map_y()

        
def view_tick():
    """Handle all of the view actions in the game loop."""
    if GC.log_updated:
        update_log_surf()

    update_eq_surf()
    update_status_surf()
    
    render_map()
    render_objects()
    render_decorations()

    # Draw all of the game surfaces on to the screen
    GV.screen.fill(GV.black, GV.logview_rect)
    GV.screen.blit(GV.log_surf, GV.logview_rect,
                   Rect(GV.logview_rect.x - GV.log_rect.x,
                        GV.logview_rect.y - GV.log_rect.y,
                        GV.logview_rect.w,
                        GV.logview_rect.h))

    GV.screen.blit(GV.eq_surf, GV.eq_rect)
    GV.screen.blit(GV.status_surf, GV.status_rect)

    # Partition off a piece of the map_surf and blit it on to the screen
    # at the location specified by the mapview_rect
    GV.screen.blit(GV.map_surf, GV.mapview_rect,
                   Rect(GV.mapview_rect.x - GV.map_rect.x,
                        GV.mapview_rect.y - GV.map_rect.y,
                        GV.mapview_rect.w,
                        GV.mapview_rect.h))

    # Draw the scrollbars
    GV.x_scrollbar.update(GV.screen)
    GV.y_scrollbar.update(GV.screen)
    GV.log_scrollbar.update(GV.screen)

    if GC.state == ST_MENU:
        GV.screen.blit(GV.dialog_surf, GV.dialog_rect)
    else:
        render_tooltips()

    pygame.display.flip()
