# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import pygame
from pygame.locals import *

from const import *

class Server:
    """Stores the server state."""
    # Debug mode
    debug = True
    
    # The map of the current level, a two dimensional array
    map = None

    branch = 'doom'
    dlevel = 1

    # A Hash of all levels.  Accessed like dlevel['doom'][1]
    dlevel_dict = {}

    # The player object
    u = None

    # Dict of all monsters and all items across all levels
    monsters_dict = {}
    items_dict = {}
    
    # List of all monsters on the current level
    monsters = []

    # All free items (not in inventory) on the current level
    items = []

    # two dimensional array showing which locations are in the field of view
    fov_map = None

    # Whether or not we need to recompute the FOV
    fov_recompute = True

    # State of the game.
    state = ST_PLAYING
    
    u_action = None

    # Messages in the game log.
    msgs = []

    # The complete history of commands used in this game
    cmd_history = []

    random_seed = None

    # The random number generator used for building maps and other data that
    # needs to be the same for all games using the same random seed.
    map_rand = None
    # The random number generator used for everything else.
    rand = None

    fov_outline = False

    # Whether or not the message log has been updated this cycle.
    log_updated = True

