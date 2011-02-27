"""AI routines.  Can be assigned to Monster objects to tell them how to behave."""

from const import *
from game import *


class StupidAI:
    """AI for a monster that tries to move next to the player and whack him."""

    def take_turn(self):
        # If I can see the monster, it can see me
        m = self.owner
        if GC.u.fov_map.lit(m.x, m.y):
 
            if m.distance_to(GC.u) >= 2:
                m.move_towards(GC.u.x, GC.u.y)
            elif GC.u.hp > 0:
                m.attack(GC.u)


        
def move_randomly(self):
    direction = random.randrange(len(DIR))
    if self.can_move_dir(DIR[direction]):
        return self.move(DIR[direction])

    
def move_towards_pc_idiot(self):
    move_direction_hor = GC.u.x - self.x
    move_direction_ver = GC.u.y - self.y

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

def move_towards_pc_random_idiot(self, random_degree=0.2):
    move_direction_hor = GC.u.x - self.x
    move_direction_ver = GC.u.y - self.y
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

def move_towards_pc(self):
    if self.int <= 10:
        self.move_towards_pc_idiot()
    elif self.int <= 20:
        self.move_towards_pc_random_idiot()
