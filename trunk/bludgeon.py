#!/usr/bin/env python

import sys
import os

try:
    import pygame
except:
    print 'Pygame is Required, http://www.pygame.org'


abspath = os.path.abspath(sys.argv[0])
dir = os.path.split(abspath)[0]
os.chdir(dir)

sys.path.append('src')
import main
main.main()
