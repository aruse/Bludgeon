# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import random
from collections import deque

from const import *


class ServerState(object):
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

    monsters_to_delete = []
    items_to_delete = []

    # Two dimensional array showing which locations are in the field of view
    fov_map = None

    mode = ST_PLAYING

    u_action = None
    u_took_turn = False

    # Messages in the game log.
    msgs = deque()

    # The complete history of commands used in this game
    cmd_history = []

    random_seed = None

    # The random number generator used for building maps and other data that
    # needs to be the same for all games using the same random seed.
    map_rand = random.Random()
    # The random number generator used for everything else.
    rand = random.Random()
