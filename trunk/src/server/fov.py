# Copyright (c) 2011, Andy Ruse

"""Routines for calculating field of view (FOV).
Based on Bjorn Bergstrom's recursive shadowcasting algorithm.
"""

class FOVMap(object):
    # Multipliers for transforming coordinates to other octants.
    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]
    def __init__(self, map):
        self.data = map
        self.w, self.h = len(map), len(map[0])
        self.marked = []
        for i in range(self.w):
            self.marked.append([0] * self.h)
        self.flag = 1

    def square(self, x, y):
        return self.data[x][y]

    def blocked(self, x, y):
        return (x < 0 or y < 0
                or x >= self.w or y >= self.h
                or self.data[x][y].block_sight)

    def in_fov(self, x, y):
        """Returns whether or not this cell is in the FOV."""
        return (0 <= x < self.w and 0 <= y < self.h
                and self.marked[x][y] == self.flag)

    def set_marked(self, x, y):
        """Sets a cell as in the FOV."""
        if 0 <= x < self.w and 0 <= y < self.h:
            self.marked[x][y] = self.flag

    def _cast_ray(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        """Recursive raycasting function"""
        if start < end:
            return
        radius_squared = radius * radius

        for j in range(row, radius+1):
            dx, dy = -j - 1, -j
            blocked = False

            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # Extremities of the square we're considering:
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self.set_marked(X, Y)
                    if blocked:
                        # We're scanning a row of blocked squares:
                        if self.blocked(X, Y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_ray(cx, cy, j + 1, start, l_slope,
                                             radius, xx, xy, yx, yy, id + 1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    def do_fov(self, x, y, radius):
        """Calculate which cells are in FOV from the given
        location and radius.
        """
        self.flag += 1
        for oct in range(8):
            self._cast_ray(x, y, 1, 1.0, 0.0, radius,
                             self.mult[0][oct], self.mult[1][oct],
                             self.mult[2][oct], self.mult[3][oct], 0)
        # This is necessary because the algorithm doesn't recognise the
        # starting square as being in the FOV.
        self.set_marked(x, y)
        
