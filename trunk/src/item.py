import random
import math

import pygame
from pygame.locals import *

from const import *
from game import *
from util import *
from mon_class import *
from fov import *
from ai import *
from object import *                    
from monster import *

class Item(Object):
    """Anything that can be picked up."""
    
    def __init__(self, x, y, name, use=None, prev_monster=None):
        Object.__init__(self, x, y, name)
        # The function to call when applying an item
        self.use = use
        self.blocks_sight = False
        self.blocks_movement = False

        # For items which were previously a monster.  Used for resurrection, de-stoning, etc.
        self.prev_monster = prev_monster
