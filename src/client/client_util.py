# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Utility functions, needed in a wide variety of places in the client code.
"""

import common.cfg as cfg
from client_state import ClientState as CS


def client_message(msg, color=None):
    """Add a message to the client game log."""
    CS.msgs.append((msg, color))
    CS.log_updated = True


def cell2pixel(x, y):
    """
    Take in (x, y) cell coords and return (x, y) pixel coords on the map
    surface.
    """
    return ((x + 1) * cfg.TILE_W, (y + 1) * cfg.TILE_H)


def quit_game(signum=None, frame=None):
    """Gracefully exit."""
    CS.mode = cfg.ST_QUIT
