#!/usr/bin/env python

# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

import unittest2
from server.room import Room

class RoomTest(unittest2.TestCase):
    dims = ((0, 0, 4, 5),
            (2, 2, 10, 10),
            (40, 50, 8, 5))

    centers = ((2, 2),
               (7, 7),
               (44, 52))

    def setUp(self):
        """Create some rooms."""
        self.rooms = []
        for dim in RoomTest.dims:
            self.rooms.append(Room(*dim))

    def test_create(self):
        """
        Test to see if rooms can be created, and if incorrect sizes
        are rejected.
        """
        room = Room(2, 2, 5, 10)
        self.assertIsInstance(room, Room)

        def create():
            room = Room(2, 2, 2, 2)
        self.assertRaises(ValueError, create)

    def test_intersect(self):
        """
        See if rooms intersect when they should, and don't intersect
        when they shouldn't.
        """
        self.assertTrue(self.rooms[0].intersect(self.rooms[0]))
        self.assertTrue(self.rooms[0].intersect(self.rooms[1]))
        self.assertTrue(self.rooms[1].intersect(self.rooms[0]))
        self.assertFalse(self.rooms[1].intersect(self.rooms[2]))
        self.assertFalse(self.rooms[2].intersect(self.rooms[1]))

    def test_center(self):
        """Make sure the centers of rooms are correct."""
        for i in range(len(self.rooms)):
            self.assertEquals(self.rooms[i].center(), RoomTest.centers[i])

if __name__ == "__main__":
    unittest2.main()
