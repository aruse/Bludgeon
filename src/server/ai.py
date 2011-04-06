# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
AI classes.  Can be assigned to Monster objects to tell them how to
behave.
"""

import cfg
from color import CLR
from server_state import ServerState as SS
from util import message


class StupidAI(object):
    """AI for a monster that tries to move next to the player and whack him."""

    def __init__(self):
        # This is the Monster object which uses this AI.  Will be set in
        # Monster.__init__
        self.owner = None

    def take_turn(self):
        """Move towards the player and whack him."""
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
    def __init__(self, old_ai, num_turns=cfg.CONFUSE_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns
        # This is the Monster object which uses this AI.  Will be set in
        # Monster.__init__
        self.owner = None

    def take_turn(self):
        """
        Move in a random direction if still confused.  If no longer confused,
        revert to the previous AI.
        """

        if self.num_turns > 0:
            self.owner.move_randomly()
            self.num_turns -= 1
        else:
            self.owner.ai = self.old_ai
            message('The ' + self.owner.name + ' is no longer confused!',
                    CLR['red'])
