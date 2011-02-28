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
from gui import *
from spell import *

class Item(Object):
    """Anything that can be picked up."""
    
    def __init__(self, x, y, name, use_function=None, prev_monster=None):
        Object.__init__(self, x, y, name)
        self.blocks_sight = False
        self.blocks_movement = False

        # For items which were previously a monster.  Used for resurrection, de-stoning, etc.
        self.prev_monster = prev_monster

        
        if self.name == 'fizzy':
            self.use_function = cast_heal
        elif self.name == 'THARR':
            self.use_function = cast_fireball
        elif self.name == 'YUM YUM':
            self.use_function = cast_lightning
        elif self.name == 'NR 9':
            self.use_function = cast_confuse
