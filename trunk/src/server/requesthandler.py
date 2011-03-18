# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""RequestHandler class and dictionaries use to map client requests to
server actions.
"""

import pygame
from pygame.locals import *

from const import *
from server.server import Server as S
from util import *
from server.monster import *
from server.item import *
from server.dlevel import *
from server.cell import *
from server.ai import *
from server.gui import *
from server.spell import *
from server.saveload import *
from stuff import *


class RequestHandler:
    """Handle a specific client request."""
    def __init__(self, action, turn, desc=None):
        """Arguments:
        @param action: Action to performed by the S.
        @param turn: Whether or not this action counts as taking a turn.  
        If this depends on the outcome of the action, set it to None and let
        the action handler take care of it.
        @param desc: Short description of what this request does.
        """
        self.action = action
        self.turn = turn

    def do(self, args):
        """Perform the action associated with this request."""
        S.u_took_turn = self.turn
        print 'Running on server:', self.action, args
        return self.action(*args)


def attach_request_actions():
    """Set up dictionaries to map requests to actions."""
    
    S.requests = {
        'm': RequestHandler(S.u.move, True, "Move the player."),
        'F': RequestHandler(S.u.attack, True, "Attack a location."),
        ',': RequestHandler(pick_up, None, "Pick up an item."),
        'd': RequestHandler(S.u.drop, None, "Drop an item."),
        'a': RequestHandler(S.u.use, None, "Use an item."),
        }

    # Define actions for special debug mode requests.
    if S.debug:
        S.requests['^f'] = RequestHandler(
            magic_mapping, False, "Map the entire level.")
