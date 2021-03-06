# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""Map class"""

import common.cfg as cfg
from server_state import ServerState as SS
from cell import Cell
from room import Room
from monster import Monster
from item import Item
import ai


class Map(object):
    """
    Map of dungeon level, containing a grid of Cell objects, and lists of
    monsters, items, and dungeon features.
    """

    def __init__(self, w, h, layout='connected_rooms'):
        self.w, self.h = w, h
        self.layout = layout

        # List of all monsters on this map
        self.monsters = []
        # List of all free items (not in inventory) on this map
        self.items = []

        self.upstairs = (0, 0)
        self.downstairs = (0, 0)

        self.grid = [[Cell('cmap, wall, dark')
                      for j in xrange(self.h)]
                     for i in xrange(self.w)]
        self.rooms = []
        self.gen_connected_rooms()

        # Set to true if this map (not the individual cells) has been modified.
        self.dirty = True

    def create_h_tunnel(self, x1, x2, y):
        """Create horizontal tunnel."""
        for x in xrange(min(x1, x2), max(x1, x2) + 1):
            self.grid[x][y].set_attr('cmap, floor of a room')

    def create_v_tunnel(self, y1, y2, x):
        """Create vertical tunnel."""
        for y in xrange(min(y1, y2), max(y1, y2) + 1):
            self.grid[x][y].set_attr('cmap, floor of a room')

    def gen_connected_rooms(self):
        """
        Generate a series of rooms, connected with vertical and horizontal
        tunnels.  Each room is connected to the previous one with one tunnel.
        """
        for i in xrange(cfg.MAX_ROOMS):
            w = SS.map_rand.randrange(cfg.MIN_ROOM_SIZE, cfg.MAX_ROOM_SIZE)
            h = SS.map_rand.randrange(cfg.MIN_ROOM_SIZE, cfg.MAX_ROOM_SIZE)
            x = SS.map_rand.randrange(0, self.w - w - 1)
            y = SS.map_rand.randrange(0, self.h - h - 1)

            new_room = Room(x, y, w, h)

            # See if any of the other rooms intersect with this one
            failed = False
            for room in self.rooms:
                if new_room.intersect(room):
                    failed = True
                    break

            if not failed:
                # First room
                if len(self.rooms) == 0:
                    (new_x, new_y) = new_room.center()
                    self.upstairs = (new_x, new_y)

                self.create_rectangular_room(new_room)
                self.place_objects(new_room)
                self.rooms.append(new_room)

        # Connect the rooms
        for j in xrange(1, len(self.rooms)):
            (new_x, new_y) = self.rooms[j].center()
            (prev_x, prev_y) = self.rooms[j - 1].center()
            if SS.map_rand.randrange(0, 2):
                self.create_h_tunnel(prev_x, new_x, prev_y)
                self.create_v_tunnel(prev_y, new_y, new_x)
            else:
                self.create_v_tunnel(prev_y, new_y, prev_x)
                self.create_h_tunnel(prev_x, new_x, new_y)

    def blocks_movement(self, x, y):
        """Return whether or not this location blocks movement."""
        if self.grid[x][y].blocks_movement:
            return True

        if SS.u.x == x and SS.u.y == y and SS.u.blocks_movement:
            return True

        for mon in self.grid[x][y].monsters:
            if mon.blocks_movement:
                return True

        for item in self.grid[x][y].items:
            if item.blocks_movement:
                return True

        return False

    def place_objects(self, room):
        """Place random objects in a room."""
        # Choose random number of monsters
        for i in xrange(SS.map_rand.randrange(cfg.MAX_ROOM_MONSTERS)):
            x = SS.map_rand.randrange(room.x1 + 1, room.x2 - 1)
            y = SS.map_rand.randrange(room.y1 + 1, room.y2 - 1)

            # Don't place monsters on the up stairs, as that's where the player
            # will be placed.
            if not self.blocks_movement(x, y) and (x, y) != self.upstairs:
                if SS.map_rand.randrange(0, 100) < 60:
                    mon = Monster(x, y, 'orc', ai=ai.StupidAI())
                else:
                    mon = Monster(x, y, 'troll', ai=ai.StupidAI())

                mon.place_on_map(self)

        # Choose random number of items
        for i in xrange(SS.map_rand.randrange(cfg.MAX_ROOM_ITEMS)):
            x = SS.map_rand.randrange(room.x1 + 1, room.x2 - 1)
            y = SS.map_rand.randrange(room.y1 + 1, room.y2 - 1)

            if not self.blocks_movement(x, y):
                dice = SS.map_rand.randrange(0, 100)
                if dice < 40:
                    item = Item(x, y, 'healing potion')
                elif dice < 40 + 20:
                    item = Item(x, y, 'scroll of fireball')
                elif dice < 40 + 20 + 20:
                    item = Item(x, y, 'scroll of lightning')
                else:
                    item = Item(x, y, 'scroll of confusion')

                item.place_on_map(self)

    def create_rectangular_room(self, room):
        """Create a rectangular room."""
        # Punch out the floor tiles
        for x in xrange(room.x1 + 1, room.x2):
            for y in xrange(room.y1 + 1, room.y2):
                self.grid[x][y].set_attr('cmap, floor of a room')

        # Add wall tiles surrounding the room
        for x in xrange(room.x1 + 1, room.x2):
            self.grid[x][room.y1].set_attr('cmap, wall, horizontal')
            self.grid[x][room.y2].set_attr('cmap, wall, horizontal')
        for y in xrange(room.y1 + 1, room.y2):
            self.grid[room.x1][y].set_attr('cmap, wall, vertical')
            self.grid[room.x2][y].set_attr('cmap, wall, vertical')

        # Add corner tiles
        self.grid[room.x1][room.y1].set_attr('cmap, wall, top left corner')
        self.grid[room.x2][room.y1].set_attr('cmap, wall, top right corner')
        self.grid[room.x1][room.y2].set_attr('cmap, wall, bottom left corner')
        self.grid[room.x2][room.y2].set_attr('cmap, wall, bottom right corner')

    def client_serialize(self):
        """Convert map to a string for transport to the client."""
        grid = [[cell.client_serialize()
                 for cell in x]
                for x in self.grid]
        return ("{{'w':{0},'h':{1},'layout':{2},'grid':{3},"
                "}}".format(
                self.w, self.h, repr(self.layout), grid))
