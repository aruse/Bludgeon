# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Routines for drawing the various surfaces in various combinations on the
screen.
"""

import pygame
from pygame import Rect, Surface
import pygame.locals as pgl

import cfg
from color import CLR
from client_state import ClientState as CS
from client_util import cell2pixel


def move_surface_locations():
    """Set the x,y coords for each of the game's surfaces."""
    CS.map_rect.x, CS.map_rect.y = 0, CS.status_rect.h
    CS.mapview_rect.x, CS.mapview_rect.y = 0, CS.status_rect.h

    CS.log_rect.x, CS.log_rect.y = 0, 0
    CS.logview_rect.x, CS.logview_rect.y = 0, 0

    CS.eq_rect.x = CS.logview_rect.w + cfg.SCROLLBAR_W
    CS.eq_rect.y = 0
    CS.status_rect.x = CS.eq_rect.x + CS.eq_rect.w
    CS.status_rect.y = 0


def handle_resize(w, h):
    """
    Shuffle surfaces around to their correct places when the game window
    is resized.
    """
    if w < cfg.MIN_LOG_W + CS.eq_rect.w + CS.status_rect.w:
        w = cfg.MIN_LOG_W + CS.eq_rect.w + CS.status_rect.w
    if h < CS.status_rect.h + cfg.MIN_MAPVIEW_H:
        h = CS.status_rect.h + cfg.MIN_MAPVIEW_H

    # Resize the main screen
    CS.screen_rect.w, CS.screen_rect.h = w, h
    CS.screen = pygame.display.set_mode((CS.screen_rect.w, CS.screen_rect.h),
                                        pygame.RESIZABLE)

    # Resize the mapview. We have to shave off a little so the scrollbars
    # can fit
    CS.mapview_rect.w = CS.screen_rect.w - cfg.SCROLLBAR_W
    CS.mapview_rect.h = CS.screen_rect.h - CS.status_rect.h - cfg.SCROLLBAR_W

    # Resize the log surface
    CS.log_rect.w = (CS.screen_rect.w - (CS.eq_rect.w + CS.status_rect.w) -
                     cfg.SCROLLBAR_W)
    CS.logview_rect.w = CS.log_rect.w

    # Resize the dialog surface
    set_dialog_size()

    # Move the surfaces to their new locations
    move_surface_locations()
    CS.log_updated = True

    CS.x_scrollbar.resize()
    CS.y_scrollbar.resize()
    CS.log_scrollbar.resize()

    center_map()


def set_dialog_size():
    """Set the rect dimensions for the dialog surface."""
    CS.dialog_rect.x = CS.screen_rect.w / 2 - CS.dialog_rect.w / 2
    CS.dialog_rect.y = CS.screen_rect.h / 2 - CS.dialog_rect.h / 2
    if CS.dialog_rect.x < 0:
        CS.dialog_rect.x = 0
    if CS.dialog_rect.y < 0:
        CS.dialog_rect.y = 0


def mouse2cell(x, y):
    """Convert mouse coords to cell coords on the map."""
    # Compensate for the relative position of the map surface.
    x -= CS.map_rect.x
    y -= CS.map_rect.y

    # Compensate for map border
    x -= cfg.TILE_W
    y -= cfg.TILE_H

    # Convert into map coords
    x /= cfg.TILE_W
    y /= cfg.TILE_H

    if x < 0 or x >= CS.map.w:
        x = None
    if y < 0 or y >= CS.map.h:
        y = None
    return x, y


def draw_box(x, y, color):
    """Draw a box around the cell at the given coords."""
    coords = cell2pixel(x, y)
    pygame.draw.rect(CS.map_surf, color,
                     Rect(coords[0], coords[1], cfg.TILE_W, cfg.TILE_H), 1)


def draw_line_between(x1, y1, x2, y2, color):
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

    pygame.draw.line(CS.map_surf, color, coords1, coords2, 1)


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
    """Render a menu."""
    padding = cfg.BORDER_W + cfg.PADDING

    # Create the header, with wordwrap
    text_img = wordwrap_img(header, w, True, CS.menu_font_color,
                            justify='left')

    header_h = text_img.get_height()
    h = len(options) * CS.font_h + header_h

    # Expand the width to fit long option names
    for option in options:
        text = ' (X) ' + option
        text_w = CS.font.size(text)[0]
        if text_w > w:
            w = text_w

    # Create a new surface on which to draw the menu
    surf_w = w + padding * 2
    surf_h = h + padding * 2
    CS.dialog_surf = Surface((surf_w, surf_h)).convert()
    img_fill(CS.dialog_surf, CS.menu_bg_img,
             Rect(surf_w + padding, surf_h + padding,
                  surf_w - padding * 2, surf_h - padding * 2))

    # Blit the header
    CS.dialog_surf.blit(text_img, (cfg.BORDER_W + cfg.PADDING,
                                   cfg.BORDER_W + cfg.PADDING))

    # Blit all the options
    y = (header_h + padding) / float(CS.font_h)
    letter_index = ord('a')
    for option in options:
        text = ' (' + chr(letter_index) + ') ' + option
        write_text(CS.dialog_surf, text, y, color=CS.menu_font_color,
                   justify='left', padding=padding)
        y += 1
        letter_index += 1

    # Make it pretty
    add_surface_border(CS.dialog_surf)
    CS.dialog_surf.set_colorkey(CLR['floor_blue'])
#    CS.dialog_surf.set_alpha(cfg.TOOLTIP_ALPHA)

    CS.dialog_rect.w, CS.dialog_rect.h = w, h
    set_dialog_size()

    CS.menu_options = options
    CS.mode = cfg.ST_MENU


def inventory_menu(header, menu_type):
    """
    Display an inventory menu.
    @param header: Text to display at the top of the menu.
    @param menu_type: Keyword identifying the type of menu.
    """
    CS.menu = menu_type

    inv = CS.u.inventory
    if len(inv) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inv]

    menu(header, options, cfg.MIN_INVENTORY_W)


def object_under_mouse():
    """Return the top object under the mouse."""
    x, y = pygame.mouse.get_pos()
    x, y = mouse2cell(x, y)

    if x is not None and y is not None and (
        CS.u.fov_map.in_fov(x, y) or CS.map.grid[x][y].explored):

        if len(CS.map.grid[x][y].monsters):
            return CS.map.grid[x][y].monsters[0]
        if len(CS.map.grid[x][y].items):
            return CS.map.grid[x][y].items[0]

    else:
        return None


def wordwrap_img(text, w, antialias, color, justify='left'):
    """
    Return a surface with the rendered text on it, wordwrapped to
    fit the given pixel width.
    """
    if color is None:
        color = CS.default_font_color

    lines = []
    line = ""
    words = text.split(' ')

    for word in words:
        test_line = line + word + " "

        if CS.font.size(test_line)[0] < w:
            line = test_line
        else:
            lines.append(line)
            line = word + " "

    lines.append(line)

    rendered_lines = []
    total_h = 0
    for line in lines:
        text_img = CS.font.render(line, antialias, color)
        rendered_lines.append(text_img)
        total_h += text_img.get_height()

    # This surface needs to have a transparent background
    # like all of the surfaces in rendered_lines.
    final_surf = Surface((w, total_h), pgl.SRCALPHA,
                                rendered_lines[0]).convert_alpha()

    y = 0
    for line in rendered_lines:
        if justify == 'left':
            x = 0
        elif justify == 'right':
            x = w - line.get_width()
        else:  # justify == 'center'
            x = w / 2 - line.get_width() / 2

        final_surf.blit(line, (x, y))
        y += line.get_height()

    return final_surf


def add_surface_border(surf):
    """Draw a border around a surface."""
    rect = surf.get_rect()

    left_x, right_x = 0, rect.w - cfg.BORDER_W
    top_y, bottom_y = 0, rect.h - cfg.BORDER_W

    for x in xrange(1, rect.w / cfg.BORDER_W):
        surf.blit(CS.tiles_img, (x * cfg.BORDER_W, top_y),
                  CS.tile_dict['explosion, fiery, top center'])
        surf.blit(CS.tiles_img, (x * cfg.BORDER_W, bottom_y),
                  CS.tile_dict['explosion, fiery, bottom center'])
    for y in xrange(1, rect.h / cfg.BORDER_W):
        surf.blit(CS.tiles_img, (left_x, y * cfg.BORDER_W),
                  CS.tile_dict['explosion, fiery, middle left'])
        surf.blit(CS.tiles_img, (right_x, y * cfg.BORDER_W),
                  CS.tile_dict['explosion, fiery, middle right'])

    surf.blit(CS.tiles_img, (left_x, top_y),
              CS.tile_dict['explosion, fiery, top left'])
    surf.blit(CS.tiles_img, (right_x, top_y),
              CS.tile_dict['explosion, fiery, top right'])
    surf.blit(CS.tiles_img, (left_x, bottom_y),
              CS.tile_dict['explosion, fiery, bottom left'])
    surf.blit(CS.tiles_img, (right_x, bottom_y),
              CS.tile_dict['explosion, fiery, bottom right'])


def render_tooltips():
    """Render the tooltip for the object under the mouse."""
    obj = object_under_mouse()
    if obj:
        if obj.__class__.__name__ == 'ClientMonster':
            hp_bar = True
        else:
            hp_bar = False

        bar_len = 100

        if CS.u.fov_map.in_fov(obj.x, obj.y):
            text = 'You see: ' + obj.name
        else:
            text = 'You remember seeing: ' + obj.name

        text_img = CS.font.render(text, True, CLR['white'])
        text_rect = text_img.get_rect()

        if hp_bar and text_rect.w < bar_len:
            surf_w = bar_len
        else:
            surf_w = text_rect.w

        surf_w += cfg.PADDING * 2 + cfg.BORDER_W * 2

        surf_h = text_rect.h + cfg.PADDING * 2 + cfg.BORDER_W * 2
        if hp_bar:
            surf_h += CS.font_h

        tooltip_surf = Surface((surf_w, surf_h)).convert()
        tooltip_surf.fill(CLR['black'])

        text_rect.centerx = surf_w / 2
        text_rect.top = cfg.BORDER_W + cfg.PADDING
        tooltip_surf.blit(text_img, text_rect)

        if hp_bar:
            render_bar(tooltip_surf,
                       cfg.BORDER_W + cfg.PADDING,
                       cfg.BORDER_W + cfg.PADDING + text_rect.h,
                       bar_len, obj.hp, obj.max_hp,
                       CS.hp_bar_color, CS.hp_bar_bg_color)
            hp_img = CS.font.render(str(obj.hp) + ' / ' + str(obj.max_hp),
                                      True, CLR['white'])
            hp_rect = hp_img.get_rect()
            hp_rect.centerx = cfg.BORDER_W + cfg.PADDING + bar_len / 2
            hp_rect.top = cfg.BORDER_W + cfg.PADDING + text_rect.h
            tooltip_surf.blit(hp_img, hp_rect)

        rect = tooltip_surf.get_rect()
        x, rect.bottom = pygame.mouse.get_pos()

        # The lower left corner of the tooltip is next to the mouse, unless
        # doing so would print the tooltip off the right side of the screen.
        if x + rect.w > CS.screen_rect.w:
            rect.right = x
        else:
            rect.left = x

        add_surface_border(tooltip_surf)
        tooltip_surf.set_colorkey(CLR['floor_blue'])
        tooltip_surf.set_alpha(cfg.TOOLTIP_ALPHA)
        CS.screen.blit(tooltip_surf, rect)


def render_debug_overlay():
    """Show FPS."""
    fps = round(CS.clock.get_fps(), 1)
    text_img = CS.font.render(str(fps) + " FPS", True, CLR['white'])
    text_rect = text_img.get_rect()
    text_rect.y = CS.mapview_rect.y
    CS.screen.blit(text_img, text_rect)


def update_eq_surf():
    """
    Update the equipment surface, displaying what I'm wearing and the most
    valuable gear in my backpack.
    """
    CS.eq_surf.fill(CLR['black'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_head, CS.tile_dict['conical hat'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_eyes, CS.tile_dict['lenses'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_neck, CS.tile_dict['oval'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_quiver, CS.tile_dict['runed dagger'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_shirt, CS.tile_dict['T-shirt'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_armor,
                    CS.tile_dict['red dragon scale mail'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_cloak, CS.tile_dict['faded pall'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_rweap, CS.tile_dict['athame'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_hands, CS.tile_dict['riding gloves'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_lweap, CS.tile_dict['long sword'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_rring, CS.tile_dict['diamond'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_lring, CS.tile_dict['wire'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_boots, CS.tile_dict['snow boots'])
    CS.eq_surf.blit(CS.tiles_img, CS.eq_light, CS.tile_dict['candle'])

    x = 0
    y = CS.eq_boots[1] + cfg.TILE_W * 1.5
    for i in CS.u.inventory:
        CS.eq_surf.blit(CS.tiles_img, (x, y), CS.tile_dict[i.name])
        x += cfg.TILE_W
        if x > CS.eq_rect.w - cfg.TILE_W:
            x = 0
            y += cfg.TILE_H
        if y > CS.eq_rect.h - cfg.TILE_H:
            break


def write_text(surf, text, line_num, justify='left',
               column=None, color=CS.default_font_color,
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

    text_img = CS.font.render(text, antialias, color)
    text_rect = text_img.get_rect()
    if justify == 'left':
        text_rect.left = left_border
    elif justify == 'right':
        text_rect.right = right_border
    else:  # justify == 'center':
        text_rect.centerx = center

    text_rect.top = surf.get_rect().top + line_num * CS.font_h
    surf.blit(text_img, text_rect)


def render_bar(surf, x, y, length, value,
               max_value, bar_color, background_color):
    """Render a partially filled bar (HP, MP, XP, etc)."""
    bar_length = int(float(value) / max_value * length)

    surf.fill(background_color, rect=pygame.Rect(x, y, length, CS.font_h - 1))
    if bar_length > 0:
        surf.fill(bar_color, rect=pygame.Rect(x, y, bar_length, CS.font_h - 1))


def update_status_surf():
    """Update the status surface."""
    surf = CS.status_surf
    rect = surf.get_rect()
    surf.fill(CS.log_bg_color)
    y = 0.5

    write_text(surf, 'Taimor the Human Male Apprentice (Chaotic)',
               0.5, justify='center')
    y += 1
    write_text(surf, 'Dungeons of Doom, Level 1', 1.5, justify='center')
    y += 1.5
    write_text(surf, 'HP', y, justify='left', column=0, padding=CS.font_w)
    render_bar(surf, rect.w / 4,
               rect.top + y * CS.font_h, rect.w * .75 - CS.font_w,
               CS.u.hp, CS.u.max_hp, CS.hp_bar_color, CS.hp_bar_bg_color)
    write_text(surf, str(CS.u.hp) + ' / ' + str(CS.u.max_hp),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'MP', y, justify='left', column=0, padding=CS.font_w)
    render_bar(surf, rect.w / 4,
               rect.top + y * CS.font_h, rect.w * .75 - CS.font_w,
               CS.u.mp, CS.u.max_mp, CS.mp_bar_color, CS.mp_bar_bg_color)
    write_text(surf, str(CS.u.mp) + ' / ' + str(CS.u.max_mp),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'XP', y, justify='left', column=0, padding=CS.font_w)
    render_bar(surf, rect.w / 4,
               rect.top + y * CS.font_h, rect.w * .75 - CS.font_w,
               CS.u.xp, CS.u.xp_next_level, CS.xp_bar_color,
               CS.xp_bar_bg_color)
    write_text(surf, str(CS.u.xp) + ' / ' + str(CS.u.xp_next_level),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'Weight', y, justify='left', column=0, padding=CS.font_w)
    render_bar(surf, rect.w / 4,
             rect.top + y * CS.font_h, rect.w * .75 - CS.font_w,
             CS.u.weight, CS.u.burdened, CLR['gray'], CLR['darker_gray'])
    write_text(surf, str(CS.u.weight) + ' / ' + str(CS.u.burdened),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'Hunger', y, justify='left', column=0, padding=CS.font_w)
    render_bar(surf, rect.w / 4,
             rect.top + y * CS.font_h, rect.w * .75 - CS.font_w,
             CS.u.hunger, CS.u.max_hunger, CLR['gray'], CLR['darker_gray'])
    write_text(surf, str(CS.u.hunger) + ' / ' + str(CS.u.max_hunger),
               y, justify='center', column=2)
    y += 1
    write_text(surf, 'Str', y, justify='right', column=0, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=CS.font_w)
    write_text(surf, 'AC', y, justify='right', column=2, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=CS.font_w)
    y += 1
    write_text(surf, 'Con', y, justify='right', column=0, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=CS.font_w)
    write_text(surf, 'Gold', y, justify='right', column=2, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=CS.font_w)
    y += 1
    write_text(surf, 'Dex', y, justify='right', column=0, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=CS.font_w)
    write_text(surf, 'Level', y, justify='right', column=2, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=CS.font_w)
    y += 1
    write_text(surf, 'Int', y, justify='right', column=0, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=CS.font_w)
    write_text(surf, 'Time', y, justify='right', column=2, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=CS.font_w)
    y += 1
    write_text(surf, 'Wis', y, justify='right', column=0, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=CS.font_w)
    write_text(surf, 'Score', y, justify='right', column=2, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=CS.font_w)
    y += 1
    write_text(surf, 'Cha', y, justify='right', column=0, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=1, padding=CS.font_w)
    write_text(surf, 'Weap Skill', y, justify='right',
               column=2, padding=CS.font_w)
    write_text(surf, str(18), y, justify='left', column=3, padding=CS.font_w)

    y += 1
    write_text(surf, 'Weapon Damage 3d8 + ' + str(6), y, justify='left',
               padding=CS.font_w)
    y += 1
    write_text(surf, 'Weapon Range ' + str(5), y, justify='left',
               padding=CS.font_w)
    y += 1
    write_text(surf, 'Hungry Burdened Confused Poisoned', y, justify='left',
               padding=CS.font_w)
    y += 1
    write_text(surf, 'Hallucinating Sick Blind Stunned', y, justify='left',
               padding=CS.font_w)


def update_log_surf():
    """Update the log surface."""
    total_h = 0
    text_imgs = []
    for line, color in reversed(CS.msgs):
        text_img = wordwrap_img(line, CS.log_rect.w - CS.font_w,
                                True, color, justify='left')
        text_rect = text_img.get_rect()

        text_imgs.append((text_img, text_rect))
        total_h += text_rect.h

    # To avoid divide-by-zero errors when there are no messages to display.
    if total_h < 1:
        total_h = 1

    CS.log_surf = Surface((CS.logview_rect.w, total_h)).convert()
    CS.log_surf.fill(CS.log_bg_color)
    CS.log_rect.h = total_h
    CS.log_rect.bottom = CS.logview_rect.bottom

    y = CS.log_rect.h
    for text_img, text_rect in text_imgs:
        y -= text_rect.h
        text_rect.top = y
        text_rect.left = CS.log_surf.get_rect().left + CS.font_w
        CS.log_surf.blit(text_img, text_rect)

    CS.log_scrollbar.resize()
    CS.log_scrollbar.align()

    # Mark the log surface as updated
    CS.log_updated = False


def render_map():
    """Draw all the map Cells onto the map surface."""
    CS.map_surf.fill(CLR['black'])

    for x in xrange(CS.map.w):
        for y in xrange(CS.map.h):
            if CS.u.fov_map.in_fov(x, y):
                CS.map.grid[x][y].draw(x, y)
                CS.map.grid[x][y].explored = True
            else:
                if CS.map.grid[x][y].explored:
                    CS.map.grid[x][y].draw_gray(x, y)
                else:
                    CS.map_surf.blit(CS.tiles_img,
                                     cell2pixel(x, y), CS.blank_tile)


def render_objects():
    """Draw all the game Objects onto the map surface."""
    for item in CS.map.items:
        if CS.u.fov_map.in_fov(item.x, item.y):
            item.draw()
        else:
            if CS.map.grid[item.x][item.y].explored:
                item.draw_gray()

    for mon in CS.map.monsters:
        if CS.u.fov_map.in_fov(mon.x, mon.y):
            mon.draw()

    # Always draw the player
    CS.u.draw()


def draw_fov_outline(color):
    """Draws an outline around the outside of any FOV maps in play."""
    for mon in CS.map.monsters + [CS.u]:
        if mon.fov_map is None:
            continue

        for x in xrange(mon.x - mon.fov_radius, mon.x + mon.fov_radius):
            for y in xrange(mon.y - mon.fov_radius, mon.y + mon.fov_radius):
                if (mon.fov_map.in_fov(x, y)
                    != mon.fov_map.in_fov(x + 1, y)):
                    draw_line_between(x, y, x + 1, y, color)
                if (mon.fov_map.in_fov(x, y)
                    != mon.fov_map.in_fov(x, y + 1)):
                    draw_line_between(x, y, x, y + 1, color)


def render_decorations():
    """
    Draw any extra stuff on top of the map surface besides map Cells
    and game Objects.
    """
    if CS.mode == cfg.ST_PLAYING:
        draw_box(CS.u.x, CS.u.y, CLR['white'])

    if CS.mode == cfg.ST_TARGETING:
        x, y = pygame.mouse.get_pos()
        x, y = mouse2cell(x, y)
        draw_box(x, y, CLR['white'])

    pygame.draw.rect(CS.map_surf, CLR['red'],
                     Rect(0, 0, CS.map_rect.w, CS.map_rect.h), 1)

    if CS.fov_outline:
        draw_fov_outline(CLR['red'])

    # Put an image in the corner where the scrollbars intersect
    # FIXME: this doesn't actually do anything
    CS.screen.blit(CS.tiles_img,
                   (CS.mapview_rect.x + CS.mapview_rect.w,
                    CS.mapview_rect.y + CS.mapview_rect.h),
                   CS.tile_dict['Cthulhu'])


def center_map_x():
    """Helper function for center_map().  Handles the horizontal coordinate."""
    if CS.map_rect.w < CS.mapview_rect.w:
        CS.map_rect.x = (CS.mapview_rect.w / 2 - CS.map_rect.w / 2 +
                         CS.mapview_rect.x)
    else:
        CS.map_rect.x = (CS.mapview_rect.w / 2 - CS.u.x * cfg.TILE_W +
                         CS.mapview_rect.x)

        if CS.map_rect.x > CS.mapview_rect.x:
            CS.map_rect.x = CS.mapview_rect.x

        min_x = CS.mapview_rect.w - CS.map_rect.w + CS.mapview_rect.x

        if CS.map_rect.x < min_x:
            CS.map_rect.x = min_x

    # Move the scrollbar slider to the correct position
    CS.x_scrollbar.align()


def center_map_y():
    """Helper function for center_map().  Handles the vertical coordinate."""
    if CS.map_rect.h < CS.mapview_rect.h:
        CS.map_rect.y = (CS.mapview_rect.h / 2 - CS.map_rect.h / 2 +
                         CS.mapview_rect.y)
    else:
        CS.map_rect.y = (CS.mapview_rect.h / 2 - CS.u.y * cfg.TILE_H +
                         CS.mapview_rect.y)

        if CS.map_rect.y > CS.mapview_rect.y:
            CS.map_rect.y = CS.mapview_rect.y

        min_y = CS.mapview_rect.h - CS.map_rect.h + CS.mapview_rect.y
        if CS.map_rect.y < min_y:
            CS.map_rect.y = min_y

    # Move the scrollbar slider to the correct position
    CS.y_scrollbar.align()


def center_map():
    """Moves the map surface so that the player appears at the center of the
    mapview.  If the map surface is smaller than the mapview, center the map
    inside of the mapview instead.
    """
    center_map_x()
    center_map_y()


def update_gui():
    """Update the various game surfaces and then flip the display."""
    if CS.log_updated:
        update_log_surf()

    update_eq_surf()
    update_status_surf()

    render_map()
    render_objects()
    render_decorations()

    # Draw all of the game surfaces on to the screen
    CS.screen.fill(CLR['black'], CS.logview_rect)
    CS.screen.blit(CS.log_surf, CS.logview_rect,
                   Rect(CS.logview_rect.x - CS.log_rect.x,
                        CS.logview_rect.y - CS.log_rect.y,
                        CS.logview_rect.w,
                        CS.logview_rect.h))

    CS.screen.blit(CS.eq_surf, CS.eq_rect)
    CS.screen.blit(CS.status_surf, CS.status_rect)

    # Partition off a piece of the map_surf and blit it on to the screen
    # at the location specified by the mapview_rect
    CS.screen.fill(CLR['black'], CS.mapview_rect)
    CS.screen.blit(CS.map_surf, CS.mapview_rect,
                   Rect(CS.mapview_rect.x - CS.map_rect.x,
                        CS.mapview_rect.y - CS.map_rect.y,
                        CS.mapview_rect.w,
                        CS.mapview_rect.h))

    # Draw the scrollbars
    CS.x_scrollbar.update(CS.screen)
    CS.y_scrollbar.update(CS.screen)
    CS.log_scrollbar.update(CS.screen)

    if CS.mode == cfg.ST_MENU:
        CS.screen.blit(CS.dialog_surf, CS.dialog_rect)
    else:
        render_tooltips()

    if CS.debug:
        render_debug_overlay()

    pygame.display.flip()
