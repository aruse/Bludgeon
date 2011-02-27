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

class Object:
    """Generic object.  Can be sub-classed into players, monsters, items, etc."""
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

        # The category of this Object: human, dwarf, lich, etc.
        self.obj_class = mon_class_dict[name]

        self.tile = create_tile(GV.tiles_img, name)
        self.gray_tile = create_tile(GV.gray_tiles_img, name)
        
        # Which color to display in text mode
        self.color = None

        self.blocks_sight = False
        self.blocks_movement = False
        
    def move(self, dx, dy=None):
        """Move dx and dy spaces, if possible."""
        if type(dx) == type(tuple()):
            dx, dy = dx[0], dx[1]
            
        if self.can_move_dir(dx, dy):
            self.x += dx
            self.y += dy
            return True
        else:
            return False

    def move_towards(self, x, y=None):
        """Move towards the x, y coords, if possible."""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]

        dx = x - self.x
        dy = y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
 
        # Normalize the distance to length 1 (preserving direction), then 
        # convert it to a movment direction.
        if dx > 0:
            x = 1
        elif dx < 0:
            x = -1
        else:
            x = 0

        if dy > 0:
            y = 1
        elif dy < 0:
            y = -1
        else:
            y = 0

        if self.can_move_dir(x, y):
            self.move(x, y)
        # If we can't move in the direction we want to, then try to move vertically or horizontally
        else:
            if self.can_move_dir(x, 0):
                self.move(x, 0)
            else:
                self.move(0, y)

    def distance_to(self, obj):
        """Distance to another object."""
        return self.distance(obj.x, obj.y)

    def distance(self, x, y):
        """Distance to coords."""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def draw(self):
        """Draw this Object on the map at the current location."""
        GV.map_surf.blit(self.tile, (self.x * TILE_PW, self.y * TILE_PH))
 
    def draw_gray(self):
        """Draw this Object on the map at the current location, grayed out."""
        GV.map_surf.blit(self.gray_tile, (self.x * TILE_PW, self.y * TILE_PH))

    def can_move_dir(self, x, y=None):
        """Can the character move in this direction?"""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
            
        return self.can_move(self.x + x, self.y + y)
        
    def can_move(self, x, y=None):
        """Can the object move into this location?"""
        if type(x) == type(tuple()):
            x, y = x[0], x[1]
            
        can_move = True

        if x < 0 or y < 0 or x >= MAP_W or y >= MAP_H:
            can_move = False

        if GC.map[x][y].block_movement:
            can_move = False

        for mon in GC.monsters:
            if x == mon.x and y == mon.y:
                can_move = False
                break
            
        return can_move
                    

class Monster(Object):
    """Anything that moves and acts under its own power.  Players and NPCs count as monsters.  Pretty much any Object that's not an Item."""
    
    def __init__(self, x, y, name, ai=None):
        Object.__init__(self, x, y, name)
        self.ai = ai
        if self.ai: # Let the AI component access its owner
            self.ai.owner = self
            
        self.blocks_sight = False
        self.blocks_movement = True

        self.death_function = None
        
        # Field of view map.
        self.fov_map = None

        if name == 'wizard':
            self.hp = 30
            self.atk_power = 5
            self.defense = 2
        elif name == 'orc':
            self.hp = 10
            self.atk_power = 3
            self.defense = 0
        elif name == 'troll':
            self.hp = 16
            self.atk_power = 4
            self.defense = 1

        self.max_hp = self.hp
            
    def set_fov_map(self, map):
        self.fov_map = FOVMap(map)

    def attack(self, target):
        """Attack target with wielded weapon."""
        damage = self.atk_power - target.defense
 
        if damage > 0:
            message(self.name.capitalize() + ' attacks ' + target.name +
                    ' for ' + str(damage) + ' hit points.')
            target.take_damage(damage)
        else:
            message(self.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')
 
    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
 
            #check for death. if there's a death function, call it
            if self.hp <= 0:
                if self.death_function:
                    self.death_function()
 
    def heal(self, amount):
        #heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        
    def try_move(self, dx, dy=None):
        """Try to move dx and dy spaces.  If there's a monster in the way, attack instead."""
        if type(dx) == type(tuple()):
            dx, dy = dx[0], dx[1]

        # the coordinates the player is moving to/attacking
        x = self.x + dx
        y = self.y + dy

        # try to find an attackable object there
        target = None

        for o in GC.monsters:
            if o.x == x and o.y == y:
                target = o
                break

        # attack if target found, move otherwise
        if target is not None:
            self.attack(target)
        else:
            self.move(dx, dy)




class Item(Object):
    """Anything that can be picked up."""
    
    def __init__(self, x, y, name, use=None):
        Object.__init__(self, x, y, name)
        # The function to call when applying an item
        self.use = use
        self.blocks_sight = False
        self.blocks_movement = False
