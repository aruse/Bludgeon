# Constant declarations.  Every other module needs to import this file.

# When measurements are given in tiles, use X, Y, W, H to indicate position and size
# When measurements are given in pixels, use PX, PY, PW, PH to indicate position and size

GAME_NAME = 'Bludgeon'
VERSION = '0.0.1'


# Max number of rooms on a single dungeon level
MAX_ROOMS = 20

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 5

# Size of various things
FONT_SIZE = 16
STATUS_H, STATUS_W = 17, 50

TILE_PW = 16
TILE_PH = 16

EQ_W = 7
EQ_H = STATUS_H

MAP_W = 60
MAP_H = 25


GAME_TITLE = GAME_NAME + ' ' + VERSION

FRAME_RATE = 20

# Number of clock cycles a key has to be held down before it's repeated.
REPEAT_DELAY = 4


# Some room generation constants
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 20

# Field of View constants
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

MAX_ROOM_MONSTERS = 3
MAX_ROOM_ITEMS = 2

MAX_MSGS = STATUS_H

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
