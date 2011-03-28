# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

from collections import deque

import pygame
from pygame.locals import *

from const import *

class Server:
    """
    Static class that stores any server state that needs to be shared      
    everywhere.
    """
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

    monsters_to_delete = []
    items_to_delete = []

    # Two dimensional array showing which locations are in the field of view
    fov_map = None

    # Whether or not we need to recompute the FOV
    fov_recompute = True

    # State of the game.
    state = ST_PLAYING
    
    u_action = None
    u_took_turn = False

    # Messages in the game log.
    msgs = deque()

    # The complete history of commands used in this game
    cmd_history = []

    random_seed = None

    # The random number generator used for building maps and other data that
    # needs to be the same for all games using the same random seed.
    map_rand = None
    # The random number generator used for everything else.
    rand = None

