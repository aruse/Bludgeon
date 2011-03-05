# AI routines.  Can be assigned to Monster objects to tell them how to behave.

from const import *
from game import *
from util import *

class StupidAI:
    """AI for a monster that tries to move next to the player and whack him."""

    def take_turn(self):
        # If I can see the monster, it can see me
        m = self.owner
        if GC.u.fov_map.in_fov(m.x, m.y):
            if m.distance_to(GC.u) >= 2:
                m.move_towards(GC.u.x, GC.u.y)
            elif GC.u.hp > 0:
                m.attack(GC.u)
        else:
            m.move_randomly()


class ConfusedAI:
    """AI for a temporarily confused monster (reverts to previous AI
    after a while).
    """
    def __init__(self, old_ai, num_turns=CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns
 
    def take_turn(self):
        if self.num_turns > 0:
            # Move in a random direction, and decrease the number of
            # turns confused
            self.owner.move_randomly()
            self.num_turns -= 1
 
        else:
            # Restore the previous AI
            self.owner.ai = self.old_ai
            message('The ' + self.owner.name + ' is no longer confused!',
                    GV.red)
 
