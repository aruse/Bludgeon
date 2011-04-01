# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""AI routines.  Can be assigned to Monster objects to tell them how to
behave.
"""

from const import *
from server_state import ServerState as SS
from util import *


class StupidAI(object):
    """AI for a monster that tries to move next to the player and whack him."""

    def take_turn(self):
        # If I can see the monster, it can see me
        mon = self.owner
        if SS.u.fov_map.in_fov(mon.x, mon.y):
            if mon.distance_to(SS.u) >= 2:
                mon.move_towards(SS.u.x, SS.u.y)
            elif SS.u.hp > 0:
                mon.attack(SS.u)
        else:
            mon.move_randomly()


class ConfusedAI(object):
    """
    AI for a temporarily confused monster (reverts to previous AI
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
                    CLR['red'])
