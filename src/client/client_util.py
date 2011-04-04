# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

from const import *
from client_state import ClientState as CS


def client_message(msg, color=None):
    """Add a message to the client game log."""
    if len(CS.msgs) >= MAX_MSGS:
        CS.msgs.popleft()
    CS.msgs.append((msg, color))
    CS.log_updated = True


def cell2pixel(x, y):
    """Take in (x, y) cell coords and return (x, y) pixel coords on the map."""
    return ((x + 1) * TILE_W, (y + 1) * TILE_H)


def quit_game(signum=None, frame=None):
    """Gracefully exit."""
    CS.mode = ST_QUIT
