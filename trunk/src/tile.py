from const import *

class Tile:
    """Map tile, representing a single location on the map."""

    def __init__(self, block_movement=False, block_sight=False):
        self.block_movement = block_movement
        self.block_signt = block_sight
        
        # All tiles start unexplored
        self.explored = False
                
        self.glyph = None
        self.bitmap = None
        self.color = None

        # Value from 0 to 1, indicating degree of illumination.
        self.illumination = None

    def dig():
        self.block_movement = False
        self.block_signt = False
