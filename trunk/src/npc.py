import os, pygame, time, random
from pygame.locals import *

from const import *
from game import *
from util import *
from pc import *

class NPC(PC):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self) # Call sprite initializer
        self.image = create_tile(name)
        self.x = MAP_W - 1
        self.y = MAP_H - 1
        self.rect = Rect(GV.map_px + self.x * TILE_PW,
                         GV.map_py + self.y * TILE_PH,
                         TILE_PW, TILE_PH)
        self.int = 15

    def move_towards_pc_idiot(self,pc):
        move_direction_hor = pc.x - self.x
        move_direction_ver = pc.y - self.y

        if move_direction_hor < 0:
            self.move(-1, 0)
        elif move_direction_hor > 0:
            self.move(1, 0)
        else:
            pass # Don't move horizontally

        if move_direction_ver < 0:
            self.move(0, -1)
        elif move_direction_ver > 0:
            self.move(0, 1)
        else:
            pass # Don't move vertically

    def move_towards_pc_random_idiot(self,pc, random_degree=0.2):
        move_direction_hor = pc.x - self.x
        move_direction_ver = pc.y - self.y
        moved = 0
        
        if random.random() < random_degree:
            moved = self.move_randomly()
        else:
            if move_direction_hor < 0 and self.can_move_dir(DIRH['l']):
                self.move(DIRH['l'])
                moved = 1
            elif move_direction_hor > 0 and self.can_move_dir(DIRH['r']):
                self.move(DIRH['r'])
                moved = 1

            # Needed to prevent walking through walls
            self.update()

            if move_direction_ver < 0 and self.can_move_dir(DIRH['u']):
                self.move(DIRH['u'])
                moved = 1
            elif move_direction_ver > 0 and self.can_move_dir(DIRH['d']):
                self.move(DIRH['d'])
                moved = 1

            if not moved:
                moved = self.move_randomly()
        
        return moved

    def move_towards_pc(self,pc):
        if self.int <= 10:
            self.move_towards_pc_idiot(pc)
        elif self.int <= 20:
            self.move_towards_pc_random_idiot(pc)
