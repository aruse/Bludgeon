# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import pygame
from pygame.locals import *

from const import *


class Client():
    """Stores the game client state."""
    tiles_img = None
    gray_tiles_img = None
    menu_bg_img = None

    tile_dict = None
    glyph_dict = None

    screen = None       # Root Surface
    log_surf = None     # Surface for the game log text
    eq_surf = None      # Surface to show player's equipment
    status_surf = None  # Surface for the character stats
    map_surf = None     # Surface for the current level map
    dialog_surf = None  # Surface for pop-up dialogs

    # Rects for the various surfaces
    log_rect = Rect(0, 0, 0, 0)
    eq_rect = Rect(0, 0, 0, 0)
    status_rect = Rect(0, 0, 0, 0)
    map_rect = Rect(0, 0, 0, 0)
    screen_rect = Rect(0, 0, 0, 0)
    dialog_rect = Rect(0, 0, 0, 0)

    logview_rect = Rect(0, 0, 0, 0)
    mapview_rect = Rect(0, 0, 0, 0)

    font = None
    font_h = None
    
    # What to blit over an area that's not visible
    blank_tile = None
    
    # Cell locations to blit equipment on the equipment panel
    eq_hands = None
    eq_rweap = None
    eq_lweap = None
    eq_rring = None
    eq_lring = None
    eq_boots = None
    eq_armor = None
    eq_shirt = None
    eq_cloak = None
    eq_neck = None
    eq_eyes = None
    eq_quiver = None
    eq_light = None
    eq_head = None

    x_scrollbar = None
    y_scrollbar = None
    log_scrollbar = None

    pkeys = None


    @classmethod
    def move_surface_locations(cls):
        """Set the x,y coords for each of the game's surfaces."""
        # Shortcut to reduce verbosity.
        C = Client

        C.map_rect.x, C.map_rect.y = 0, C.status_rect.h
        C.mapview_rect.x, C.mapview_rect.y = 0, C.status_rect.h

        C.log_rect.x, C.log_rect.y = 0, 0
        C.logview_rect.x, C.logview_rect.y = 0, 0

        C.eq_rect.x = C.logview_rect.w + SCROLLBAR_W
        C.eq_rect.y = 0
        C.status_rect.x = C.eq_rect.x + C.eq_rect.w
        C.status_rect.y = 0

    @classmethod
    def init_client(cls):
        """Initialiaze class variables."""
        # Shortcut to reduce verbosity.
        C = Client

        C.font = pygame.font.SysFont('Arial', FONT_SIZE)
        C.font_h = C.font.get_height()
        C.font_w = C.font.size('X')[0]

        # Size of the map surface
        C.map_rect.w = (MAP_W + 2) * TILE_W 
        C.map_rect.h = (MAP_H + 2) * TILE_H

        # Size of the status panel
        C.status_rect.w = STATUS_W * C.font_w
        C.status_rect.h = STATUS_H * C.font_h

        # Size of the equipment panel
        C.eq_rect.w = EQ_W * TILE_W
        C.eq_rect.h = C.status_rect.h

        # Size of the full game screen
        C.screen_rect.w = C.eq_rect.w + C.status_rect.w + MIN_LOG_W
        if C.screen_rect.w < INIT_SCREEN_W:
            C.screen_rect.w = INIT_SCREEN_W

        C.screen_rect.h = C.status_rect.h + MIN_MAPVIEW_H
        if C.screen_rect.h < INIT_SCREEN_H:
            C.screen_rect.h = INIT_SCREEN_H

        # Size of the log surface
        C.log_rect.w = C.screen_rect.w - (
            C.eq_rect.w + C.status_rect.w) - SCROLLBAR_W - 50
        C.log_rect.h = C.status_rect.h
        C.logview_rect.w, C.logview_rect.h = (C.log_rect.w, C.log_rect.h)


        # The mapview size.  May be smaller or larger than the actual map size.
        # This is the location on the screen where the map or a piece thereof
        # is drawn.  It's not an actual surface, but a logical rectangle.
        C.mapview_rect.w = C.screen_rect.w - SCROLLBAR_W
        C.mapview_rect.h = (
            C.screen_rect.h - C.status_rect.h - SCROLLBAR_W)

        # Locations to blit equipment on the equipment panel
        eq_cent = (int(C.eq_rect.w / 2.0 - TILE_W / 2),
                   int(C.eq_rect.h / 2.0 - TILE_W / 2))
        C.eq_hands = (eq_cent[0], eq_cent[1])
        C.eq_hands = (eq_cent[0], C.eq_rect.y + TILE_H / 2 + 3 * TILE_H)
        C.eq_rweap = (C.eq_hands[0] - TILE_W, C.eq_hands[1])
        C.eq_lweap = (C.eq_hands[0] + TILE_W, C.eq_hands[1])
        C.eq_rring = (C.eq_hands[0] - TILE_W, C.eq_hands[1] + TILE_H)
        C.eq_lring = (C.eq_hands[0] + TILE_W, C.eq_hands[1] + TILE_H)
        C.eq_boots = (C.eq_hands[0], C.eq_hands[1] + TILE_H * 2)
        C.eq_armor = (C.eq_hands[0], C.eq_hands[1] - TILE_H)
        C.eq_shirt = (C.eq_hands[0] - TILE_W, C.eq_hands[1] - TILE_H)
        C.eq_cloak = (C.eq_hands[0] + TILE_W, C.eq_hands[1] - TILE_H)
        C.eq_neck = (C.eq_hands[0], C.eq_hands[1] - TILE_H * 2)
        C.eq_eyes = (C.eq_hands[0] - TILE_W, C.eq_hands[1] - TILE_H * 2)
        C.eq_quiver = (C.eq_hands[0] + TILE_W * 2, C.eq_hands[1] - TILE_H * 3)
        C.eq_light = (C.eq_hands[0] - TILE_W * 2, C.eq_hands[1] - TILE_H * 3)
        C.eq_head = (C.eq_hands[0], C.eq_hands[1] - TILE_H * 3)
