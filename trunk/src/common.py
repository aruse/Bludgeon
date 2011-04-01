# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import pygame
from pygame.locals import *

from const import *


def impossible(text):
    print 'Impossible area of code reached'
    print text
    exit(0)


def flatten_args(x, y):
    if isinstance(x, tuple):
        return x[0], x[1]
    else:
        return x, y
