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
        else:
            m.move_randomly()
