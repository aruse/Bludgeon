# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
RequestHandler class and dictionaries use to map client requests to
server actions.
"""

from const import *
from server_state import ServerState as SS
from object import Object
from monster import Monster
from item import Item
from dlevel import *
from cell import Cell
from ai import *
from spell import *
from saveload import *
from util import *


def pick_up(oids):
    """Try to pick up one or more items at the player's feet."""
    item_here = False

    for oid in oids:
        item = Object.obj_dict[oid]
        if item in SS.map.grid[SS.u.x][SS.u.y].items:
            SS.u.pick_up(item)
            item_here = True

    if item_here:
        SS.u_took_turn = True
    else:
        SS.u_took_turn = False
        message('Nothing to pick up!')


def magic_mapping():
    """Reveal all tiles on the map."""
    for x in xrange(SS.map.w):
        for y in xrange(SS.map.h):
            SS.map.grid[x][y].explored = True


class RequestHandler(object):
    """Handle a specific client request."""
    def __init__(self, action, turn, desc=None):
        """Arguments:
        @param action: Action to performed by the SS.
        @param turn: Whether or not this action counts as taking a turn.
        If this depends on the outcome of the action, set it to None and let
        the action handler take care of it.
        @param desc: Short description of what this request does.
        """
        self.action = action
        self.turn = turn

    def do(self, args):
        """Perform the action associated with this request."""
        SS.u_took_turn = self.turn
        return self.action(*args)


def attach_request_actions():
    """Set up dictionaries to map requests to actions."""

    SS.requests = {
        'm': RequestHandler(SS.u.move, True, "Move the player."),
        'F': RequestHandler(SS.u.attack, True, "Attack a location."),
        ',': RequestHandler(pick_up, None, "Pick up an item."),
        'd': RequestHandler(SS.u.drop, None, "Drop an item."),
        'a': RequestHandler(SS.u.use, None, "Use an item."),
        }

    # Define actions for special debug mode requests.
    if SS.debug:
        SS.requests['^f'] = RequestHandler(
            magic_mapping, False, "Map the entire level.")
