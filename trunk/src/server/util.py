# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

from const import *
from server_state import ServerState as SS

def message(msg, color=None):
    """
    Add a message to the server game log.  These messages will be passed
    directly to the client.
    """
    SS.msgs.append((msg, color))
