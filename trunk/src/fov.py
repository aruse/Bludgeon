# Copyright (c) 2011 Andy Ruse.
# See LICENSE for details.

"""
Routines for calculating field of view (FOV).
Based on Bjorn Bergstrom's recursive shadowcasting algorithm.
"""

class FOVMap(object):
    # Multipliers for transforming coordinates to other octants.
    mult = [[1,  0,  0, -1, -1,  0,  0,  1],
            [0,  1, -1,  0,  0, -1,  1,  0],
            [0,  1,  1,  0,  0, -1, -1,  0],
            [1,  0,  0,  1, -1,  0,  0, -1]]

    def __init__(self, grid):
        self.grid = grid
        self.w, self.h = len(grid), len(grid[0])
        self.marked = []
        for i in xrange(self.w):
            self.marked.append([0] * self.h)
        self.flag = 1

    def blocked(self, x, y):
        return (x < 0 or y < 0
                or x >= self.w or y >= self.h
                or self.grid[x][y].blocks_sight)

    def in_fov(self, x, y):
        """Return whether or not this cell is in the FOV."""
        return (0 <= x < self.w and 0 <= y < self.h
                and self.marked[x][y] == self.flag)

    def set_marked(self, x, y):
        """Set a cell as in the FOV."""
        if 0 <= x < self.w and 0 <= y < self.h:
            self.marked[x][y] = self.flag

    def _cast_ray(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        """Recursive raycasting function"""
        if start < end:
            return

        for i in xrange(row, radius+1):
            dx = -i - 1
            dy = -i
            blocked = False

            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into grid coordinates.
                x = cx + dx * xx + dy * xy
                y = cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering.
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square, so light it.
                    if dx ** 2 + dy ** 2 < radius ** 2:
                        self.set_marked(x, y)
                    if blocked:
                        # We're scanning a row of blocked squares.
                        if self.blocked(x, y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(x, y) and i < radius:
                            # This is a blocking square; start a
                            # recursive scan.
                            blocked = True
                            self._cast_ray(cx, cy, i + 1, start, l_slope,
                                           radius, xx, xy, yx, yy, id + 1)
                            new_start = r_slope
            # This row is scanned; do the next row unless the last square was
            # blocked.
            if blocked:
                break

    def do_fov(self, x, y, radius):
        """
        Calculate which cells are in FOV from the given location and radius.
        """
        self.flag += 1
        for oct in xrange(8):
            self._cast_ray(x, y, 1, 1.0, 0.0, radius,
                           self.mult[0][oct], self.mult[1][oct],
                           self.mult[2][oct], self.mult[3][oct], 0)
        # This is necessary because the algorithm doesn't recognise the
        # starting square as being in the FOV.
        self.set_marked(x, y)
        
