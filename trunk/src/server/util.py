# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import pygame
from pygame.locals import *

from const import *
from server import Server as S

def message(msg, color=None):
    """
    Add a message to the server game log.  These messages will be passed
    directly to the client.
    """
    S.msgs.append((msg, color))
