# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Constant declarations.
"""

GAME_NAME = 'Bludgeon'
VERSION = '0.0.1'

BUTTON_L = 1
BUTTON_M = 2
BUTTON_R = 3
BUTTON_SCROLL_U = 4
BUTTON_SCROLL_D = 5

# FIXME: dummy values
HEAL_AMOUNT = 4
LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5
CONFUSE_RANGE = 8
CONFUSE_TURNS = 10
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12

# Max number of rooms on a single dungeon level
MAX_ROOMS = 20

#ROOM_MAX_SIZE = 10
#ROOM_MIN_SIZE = 3
MAX_ROOM_SIZE = 5
MIN_ROOM_SIZE = 4

# Size of various things
FONT_SIZE = 12
STATUS_H, STATUS_W = 18, 40

# Tile size, in pixels
TILE_W, TILE_H = 16, 16

# Surface sizes, in cells
EQ_W, EQ_H = 7, STATUS_H
#MAP_W, MAP_H = 120, 50
MAP_W, MAP_H = 45, 18
#MAP_W, MAP_H = 12, 12

# Initial size of the screen, in pixels
INIT_SCREEN_W, INIT_SCREEN_H = 800, 600

# Minimum width of the log surface, in pixels
MIN_LOG_W = 200
# Minimum height of the mapview, in pixels
MIN_MAPVIEW_H = 150

# Width of the border and padding for pop-over surfaces
BORDER_W = TILE_W
PADDING = 3

GAME_TITLE = GAME_NAME + ' ' + VERSION

FRAME_RATE = 20


# Field of View constants
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

MAX_ROOM_MONSTERS = 3
MAX_ROOM_ITEMS = 8

MAX_MSGS = 100

# Up, down, left, right, upleft, upright, downleft, downright
DIR = ((0, -1),
       (0, 1),
       (-1, 0),
       (1, 0),
       (-1, -1),
       (1, -1),
       (-1, 1),
       (1, 1)
       )

# Same as above, but in a dict so we can refer to them by name.
DIRH = {'u': (0, -1),
        'd': (0, 1),
        'l': (-1, 0),
        'r': (1, 0),
        'ul': (-1, -1),
        'ur': (1, -1),
        'dl': (-1, 1),
        'dr': (1, 1)
        }


# Game state
ST_PLAYING = 1
ST_MENU = 2
ST_TARGETING = 3
ST_QUIT = 4
ST_PLAYBACK = 5

# Transparency of tooltip popups, 0-255
TOOLTIP_ALPHA = 190

# Minimum width of the inventory window, in pixels.
MIN_INVENTORY_W = 300


# Text
USE_HEADER = ('Press the key next to an item to use it, '
              'or any other to cancel.')
DELETE_HEADER = ('Press the key next to an item to use it, '
                 'or any other to cancel.')

SCROLLBAR_W = 16

# Amount to scroll a surface when using shift + direction.
SCROLL_AMT = 10
